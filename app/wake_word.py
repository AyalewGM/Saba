"""Wake word detection for Saba voice assistant."""

import asyncio
from typing import Callable, Optional
from dataclasses import dataclass
import re

from .config import config


@dataclass
class WakeWordEvent:
    """Event triggered when wake word is detected."""
    confidence: float
    timestamp: float
    audio_data: Optional[bytes] = None


class WakeWordDetector:
    """Simple wake word detector for Saba."""
    
    def __init__(self, wake_word: str = None, threshold: float = None):
        self.wake_word = wake_word or config.wake_word
        self.threshold = threshold or config.wake_word_threshold
        self.is_listening = False
        self.callbacks = []
        
        # Simple pattern matching for wake word variants
        self.wake_patterns = [
            self.wake_word,  # Exact match
            "ሳባ",  # Amharic "Saba"
            "saba",  # Latin "saba"
            "ሳባን",  # Amharic with object marker
        ]
        
    def add_callback(self, callback: Callable[[WakeWordEvent], None]):
        """Add a callback to be called when wake word is detected."""
        self.callbacks.append(callback)
        
    def remove_callback(self, callback: Callable[[WakeWordEvent], None]):
        """Remove a callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            
    async def detect_in_text(self, text: str) -> bool:
        """Detect wake word in transcribed text."""
        text_lower = text.lower().strip()
        
        # Check for wake word patterns
        for pattern in self.wake_patterns:
            if pattern.lower() in text_lower:
                confidence = self._calculate_confidence(text_lower, pattern.lower())
                if confidence >= self.threshold:
                    event = WakeWordEvent(confidence=confidence, timestamp=asyncio.get_event_loop().time())
                    await self._trigger_callbacks(event)
                    return True
                    
        return False
        
    def _calculate_confidence(self, text: str, pattern: str) -> float:
        """Calculate confidence score for wake word detection."""
        # Simple confidence based on exact match and context
        if pattern in text:
            # Higher confidence for exact word boundaries
            if re.search(rf'\b{re.escape(pattern)}\b', text):
                return 0.9
            # Lower confidence for partial matches
            return 0.7
        return 0.0
        
    async def _trigger_callbacks(self, event: WakeWordEvent):
        """Trigger all registered callbacks."""
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                # Log error but don't stop other callbacks
                print(f"Error in wake word callback: {e}")
                
    def start_listening(self):
        """Start listening for wake word."""
        self.is_listening = True
        
    def stop_listening(self):
        """Stop listening for wake word."""
        self.is_listening = False
        
    async def process_audio_stream(self, audio_data: bytes) -> bool:
        """Process audio stream for wake word detection."""
        if not self.is_listening:
            return False
            
        # For now, this is a placeholder - in a real implementation,
        # this would use an ASR model to transcribe the audio first
        # and then check for wake words
        
        # Placeholder: assume audio processing happens elsewhere
        # and we just check if we should be listening
        return False


class ConversationState:
    """Manages conversation state and flow."""
    
    def __init__(self):
        self.is_active = False
        self.last_interaction = None
        self.context = {}
        self.session_id = None
        
    def start_conversation(self, session_id: str = None):
        """Start a new conversation session."""
        self.is_active = True
        self.session_id = session_id or f"session_{asyncio.get_event_loop().time()}"
        self.context = {"session_start": asyncio.get_event_loop().time()}
        self.last_interaction = asyncio.get_event_loop().time()
        
    def end_conversation(self):
        """End the current conversation session."""
        self.is_active = False
        self.context = {}
        self.session_id = None
        self.last_interaction = None
        
    def update_context(self, key: str, value):
        """Update conversation context."""
        self.context[key] = value
        self.last_interaction = asyncio.get_event_loop().time()
        
    def is_conversation_timeout(self, timeout_seconds: int = 30) -> bool:
        """Check if conversation has timed out."""
        if not self.is_active or self.last_interaction is None:
            return False
            
        current_time = asyncio.get_event_loop().time()
        return (current_time - self.last_interaction) > timeout_seconds


class VoiceAssistantCore:
    """Core voice assistant functionality combining wake word detection and conversation."""
    
    def __init__(self):
        self.wake_detector = WakeWordDetector()
        self.conversation = ConversationState()
        self.wake_detector.add_callback(self._on_wake_word_detected)
        
    async def _on_wake_word_detected(self, event: WakeWordEvent):
        """Handle wake word detection."""
        print(f"Wake word detected with confidence {event.confidence}")
        self.conversation.start_conversation()
        
        # In a real implementation, this would trigger:
        # 1. Audio recording
        # 2. Speech-to-text
        # 3. Intent processing
        # 4. Response generation
        # 5. Text-to-speech
        
    async def process_voice_input(self, text: str) -> Optional[str]:
        """Process voice input and return response."""
        # Check for wake word if conversation is not active
        if not self.conversation.is_active:
            wake_detected = await self.wake_detector.detect_in_text(text)
            if wake_detected:
                return "ሰላም! እንዴት ልረዳሽ? Hello! How can I help you?"
            return None
            
        # Process input if conversation is active
        from .skills import skill_manager
        
        # Update conversation context
        self.conversation.update_context("last_input", text)
        
        # Handle input through skill manager
        response = await skill_manager.handle_input(text, self.conversation.context)
        
        # End conversation if requested
        if response.end_conversation:
            self.conversation.end_conversation()
            
        return response.text
        
    def start_listening(self):
        """Start listening for wake word."""
        self.wake_detector.start_listening()
        
    def stop_listening(self):
        """Stop listening."""
        self.wake_detector.stop_listening()
        self.conversation.end_conversation()


# Global voice assistant instance
voice_assistant = VoiceAssistantCore()