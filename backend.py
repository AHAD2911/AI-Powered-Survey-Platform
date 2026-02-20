"""
VIVA - AI-Powered Survey Interview System
This module provides functionality for conducting AI-powered survey interviews
with speech recognition and text generation capabilities.
"""

import google.generativeai as genai
import sqlite3
import time
import uuid
import speech_recognition as sr
import io
import os
import re

# =============================================================================
# CONFIGURATION SECTION
# =============================================================================

# Get API key from environment variable for security
API_KEY = os.getenv("GOOGLE_API_KEY", "") 
genai.configure(api_key=API_KEY)

# Pre-initialize the AI model for better performance
MODEL = genai.GenerativeModel('gemini-2.0-flash') 

# Configuration for AI response generation - optimized for speed
GEN_CONFIG = genai.GenerationConfig(
    max_output_tokens=100,  # Limited tokens for faster, concise responses
    temperature=0.7,        # Balance between creativity and consistency
    top_p=0.8,              # Controls response diversity
    top_k=40                # Limits vocabulary choices for speed
)

# Safety settings to minimize content filtering
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# =============================================================================
# DATABASE SETUP
# =============================================================================

# Create database connection with performance optimizations
CONN = sqlite3.connect("viva.db", check_same_thread=False)
# Enable Write-Ahead Logging for better concurrency
CONN.execute("PRAGMA journal_mode=WAL;")
# Reduce synchronous writes for better performance
CONN.execute("PRAGMA synchronous=NORMAL;")
CURSOR = CONN.cursor()

def init_db():
    """
    Initialize database tables for storing surveys and conversation messages.
    Creates two main tables:
    - surveys: Stores survey metadata and status
    - messages: Stores all conversation messages between AI and user
    """
    # Create surveys table if it doesn't exist
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS surveys (
            id TEXT PRIMARY KEY,          -- Unique identifier for each survey
            question TEXT,                -- Main survey question
            probes INTEGER,               -- Number of follow-up questions allowed
            length INTEGER,               -- Expected conversation length
            language TEXT,                -- Language for the conversation
            status TEXT,                  -- "Incomplete" or "Completed"
            created_at TEXT               -- Timestamp of survey creation
        )
    """)
    
    # Create messages table if it doesn't exist
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing message ID
            survey_id TEXT,               -- Links to surveys table
            role TEXT,                    -- "ai" or "user"
            content TEXT,                 -- Message content
            is_audio BOOLEAN,             -- Whether message originated from audio
            timestamp TEXT                -- When message was created
        )
    """)
    CONN.commit()

# Initialize database on module import
init_db()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def clean_ai_response(response):
    """
    Clean and sanitize AI responses by removing HTML tags and formatting.
    
    Args:
        response (str): Raw AI response text
        
    Returns:
        str: Cleaned text with HTML tags removed and whitespace normalized
    """
    if not response:
        return response
    
    # Remove all HTML tags using regex
    clean_text = re.sub(r'<.*?>', '', response)
    
    # Remove specific problematic HTML elements
    clean_text = re.sub(r'</?div[^>]*>', '', clean_text)
    clean_text = re.sub(r'</?span[^>]*>', '', clean_text)
    clean_text = re.sub(r'</?p[^>]*>', '', clean_text)
    
    # Normalize whitespace (multiple spaces/tabs/newlines to single space)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.strip()
    
    return clean_text

# =============================================================================
# AI & SPEECH PROCESSING FUNCTIONS
# =============================================================================

def transcribe_audio(audio_bytes):
    """
    Convert speech audio to text using Google Speech Recognition.
    
    Args:
        audio_bytes (bytes): Audio data in bytes format
        
    Returns:
        str: Transcribed text or error message if transcription fails
    """
    recognizer = sr.Recognizer()
    try:
        # Convert bytes to file-like object for speech recognition
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source) 
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError:
        return "Error: Speech recognition API unavailable"
    except Exception as error:
        return f"Error: {str(error)}"

def generate_ai_response(messages, user_input, survey_question, probes_asked, limit):
    """
    Generate AI responses for survey conversations with optimized performance.
    
    Args:
        messages (list): Previous conversation messages
        user_input (str): Latest user input to respond to
        survey_question (str): Original survey question
        probes_asked (int): Number of probes asked so far
        limit (int): Maximum number of probes allowed
        
    Returns:
        str: AI-generated response or fallback message
    """
    try:
        # Calculate actual probes (excluding the initial question)
        actual_probes_asked = max(0, probes_asked - 1)
        
        # Check if interview is complete (reached probe limit)
        if actual_probes_asked >= limit:
            return "Thank you for your participation! This interview is now complete."
        
        # Generate appropriate prompt based on conversation stage
        if probes_asked == 1:  # First follow-up question
            prompt = f"Ask one follow-up about: {user_input}. Max 10 words."
        else:
            # For subsequent questions, use recent context for better continuity
            recent_context = ""
            if len(messages) >= 4:  # Ensure we have enough conversation history
                recent_context = f"Previous: {messages[-2]['content']} - {messages[-1]['content']}"
            
            prompt = f"Follow-up on: {user_input}. {recent_context} Max 10 words."

        # Generate AI response with error handling
        try:
            response = MODEL.generate_content(
                prompt, 
                generation_config=GEN_CONFIG,
                safety_settings=SAFETY_SETTINGS
            )
            
            # Extract text from response with multiple fallback methods
            try:
                raw_response = response.text
            except ValueError:
                # Fallback extraction method if primary fails
                if response.candidates and response.candidates[0].content.parts:
                    raw_response = response.candidates[0].content.parts[0].text
                else:
                    raw_response = "Can you tell me more about that?"
            
            # Clean and return the response
            clean_response = clean_ai_response(raw_response)
            return clean_response
            
        except Exception as api_error:
            # Fallback responses if AI service is unavailable or slow
            fallback_responses = [
                "That's interesting. Can you tell me more?",
                "What else can you share about that?",
                "I'd love to hear more details.",
                "Could you elaborate on that?",
                "What makes you say that?"
            ]
            return fallback_responses[actual_probes_asked % len(fallback_responses)]

    except Exception as error:
        # Final safety net for any unexpected errors
        return "Thank you for sharing. What else would you like to add?"

# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

def create_survey_record(question, probes, length, language):
    """
    Create a new survey record in the database.
    
    Args:
        question (str): The main survey question
        probes (int): Number of allowed follow-up questions
        length (int): Expected conversation length
        language (str): Language for the conversation
        
    Returns:
        str: Unique survey ID for the created survey
    """
    survey_id = str(uuid.uuid4())  # Generate unique identifier
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    
    # Insert survey metadata
    CURSOR.execute(
        "INSERT INTO surveys VALUES (?, ?, ?, ?, ?, ?, ?)",
        (survey_id, question, probes, length, language, "Incomplete", created_at)
    )
    
    # Record the initial AI question as first message
    CURSOR.execute(
        "INSERT INTO messages (survey_id, role, content, is_audio, timestamp) VALUES (?, ?, ?, ?, ?)",
        (survey_id, "ai", question, False, created_at)
    )
    
    CONN.commit()
    return survey_id

def get_all_surveys(status="Incomplete"):
    """
    Retrieve all surveys with specified status.
    
    Args:
        status (str): Filter surveys by status ("Incomplete" or "Completed")
        
    Returns:
        list: List of survey dictionaries ordered by creation date (newest first)
    """
    CURSOR.execute("SELECT * FROM surveys WHERE status=? ORDER BY created_at DESC", (status,))
    columns = [desc[0] for desc in CURSOR.description]  # Get column names
    return [dict(zip(columns, row)) for row in CURSOR.fetchall()]  # Convert to dict

def get_survey_by_id(survey_id):
    """
    Retrieve a specific survey by its unique ID.
    
    Args:
        survey_id (str): The unique survey identifier
        
    Returns:
        dict: Survey data as dictionary or None if not found
    """
    CURSOR.execute("SELECT * FROM surveys WHERE id=?", (survey_id,))
    row = CURSOR.fetchone()
    if row:
        columns = [desc[0] for desc in CURSOR.description]
        return dict(zip(columns, row))
    return None

def get_messages(survey_id):
    """
    Retrieve all messages for a specific survey in chronological order.
    
    Args:
        survey_id (str): The unique survey identifier
        
    Returns:
        list: List of message dictionaries ordered by timestamp
    """
    CURSOR.execute("SELECT * FROM messages WHERE survey_id=? ORDER BY id ASC", (survey_id,))
    columns = [desc[0] for desc in CURSOR.description]
    return [dict(zip(columns, row)) for row in CURSOR.fetchall()]

def add_message(survey_id, role, content, is_audio=False):
    """
    Add a new message to the conversation history.
    
    Args:
        survey_id (str): The unique survey identifier
        role (str): "ai" or "user" - who sent the message
        content (str): The message content
        is_audio (bool): Whether the message originated from audio input
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    CURSOR.execute(
        "INSERT INTO messages (survey_id, role, content, is_audio, timestamp) VALUES (?, ?, ?, ?, ?)",
        (survey_id, role, content, is_audio, timestamp)
    )
    CONN.commit()

def mark_survey_complete(survey_id):
    """
    Mark a survey as completed in the database.
    
    Args:
        survey_id (str): The unique survey identifier to mark as complete
    """
    CURSOR.execute("UPDATE surveys SET status='Completed' WHERE id=?", (survey_id,))
    CONN.commit()

def delete_survey_record(survey_id):
    """
    Permanently delete a survey and all its associated messages.
    
    Args:
        survey_id (str): The unique survey identifier to delete
    """
    CURSOR.execute("DELETE FROM surveys WHERE id=?", (survey_id,))
    CURSOR.execute("DELETE FROM messages WHERE survey_id=?", (survey_id,))
    CONN.commit()