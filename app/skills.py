"""Base skill framework for Saba voice assistant."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re


@dataclass
class SkillResponse:
    """Response from a skill."""
    text: str
    speech: Optional[str] = None  # Different text for TTS if needed
    end_conversation: bool = False
    data: Optional[Dict[str, Any]] = None


class Skill(ABC):
    """Base class for all Saba skills."""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def can_handle(self, text: str, context: Dict[str, Any]) -> bool:
        """Check if this skill can handle the given input."""
        pass
        
    @abstractmethod
    async def handle(self, text: str, context: Dict[str, Any]) -> SkillResponse:
        """Handle the user input and return a response."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this skill does."""
        pass


class WeatherSkill(Skill):
    """Skill for weather-related queries in Amharic."""
    
    def __init__(self):
        super().__init__("weather")
        # Amharic weather keywords
        self.weather_keywords = [
            "ሰማይ", "ዝናብ", "ፀሐይ", "ንፋስ", "ሙቀት", "ቅዝቃዜ",  # weather terms
            "weather", "rain", "sun", "wind", "temperature", "cold", "hot"
        ]
        
    def can_handle(self, text: str, context: Dict[str, Any]) -> bool:
        """Check if input is weather-related."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.weather_keywords)
        
    async def handle(self, text: str, context: Dict[str, Any]) -> SkillResponse:
        """Handle weather queries."""
        # Simple placeholder response in Amharic
        return SkillResponse(
            text="ይቅርታ፣ የሰማይ ሁኔታ አገልግሎት አሁንም እየተገነባ ነው። Weather service is still under development.",
            speech="ይቅርታ፣ የሰማይ ሁኔታ አገልግሎት አሁንም እየተገነባ ነው።"
        )
        
    @property
    def description(self) -> str:
        return "Provides weather information in Amharic"


class GreetingSkill(Skill):
    """Skill for handling greetings in Amharic."""
    
    def __init__(self):
        super().__init__("greeting")
        self.greeting_patterns = [
            r"(ሰላም|hello|hi|hey)",
            r"(እንዴት\s*ነህ|እንዴት\s*ነሽ|how\s*are\s*you)",
            r"(ጤና\s*ይስጥልኝ|good\s*morning|good\s*afternoon|good\s*evening)",
            r"(ውብ\s*ጠዋት|good\s*day)",
        ]
        
    def can_handle(self, text: str, context: Dict[str, Any]) -> bool:
        """Check if input is a greeting."""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.greeting_patterns)
        
    async def handle(self, text: str, context: Dict[str, Any]) -> SkillResponse:
        """Handle greetings."""
        responses = [
            "ሰላም! እንዴት ነህ? ሳባ እኔ ነኝ፣ የአማርኛ ድምጽ ረዳት። Hello! I'm Saba, your Amharic voice assistant.",
            "ጤና ይስጥልኝ! ምን ልረዳሽ? Good day! How can I help you?",
            "ውብ ጠዋት! ሳባ ለአገልግሎትሽ ዝግጁ ነች። Good morning! Saba is ready to serve you."
        ]
        
        # Simple response selection based on time or random
        response = responses[0]  # Default to first response
        
        return SkillResponse(
            text=response,
            speech=response.split('.')[0]  # Use only Amharic part for speech
        )
        
    @property
    def description(self) -> str:
        return "Handles greetings and introductions in Amharic"


class QuestionAnsweringSkill(Skill):
    """Basic Q&A skill for Amharic."""
    
    def __init__(self):
        super().__init__("qa")
        self.qa_keywords = [
            "ማን", "ምን", "መቼ", "የት", "እንዴት", "ለምን",  # Amharic question words
            "what", "who", "when", "where", "how", "why"
        ]
        
    def can_handle(self, text: str, context: Dict[str, Any]) -> bool:
        """Check if input is a question."""
        text_lower = text.lower()
        return (any(keyword in text_lower for keyword in self.qa_keywords) or 
                text.strip().endswith('?'))
        
    async def handle(self, text: str, context: Dict[str, Any]) -> SkillResponse:
        """Handle basic questions."""
        # Simple responses for common questions
        if "ማን" in text or "who" in text.lower():
            return SkillResponse(
                text="ሳባ እኔ ነኝ፣ የአማርኛ ድምጽ ረዳት። I am Saba, an Amharic voice assistant.",
                speech="ሳባ እኔ ነኝ፣ የአማርኛ ድምጽ ረዳት።"
            )
        elif "ምን" in text or "what" in text.lower():
            return SkillResponse(
                text="እኔ የአማርኛ ሰዎችን ድምጽ በመጠቀም ለመርዳት የተሰራሁ ረዳት ነኝ። I am an assistant built to help Amharic speakers using voice.",
                speech="እኔ የአማርኛ ሰዎችን ድምጽ በመጠቀም ለመርዳት የተሰራሁ ረዳት ነኝ።"
            )
        else:
            return SkillResponse(
                text="ይቅርታ፣ ያንን ጥያቄ መመለስ አልችልም። እባክሽ እንደገና ሞክሪ። Sorry, I cannot answer that question. Please try again.",
                speech="ይቅርታ፣ ያንን ጥያቄ መመለስ አልችልም።"
            )
            
    @property
    def description(self) -> str:
        return "Answers basic questions in Amharic"


class SkillManager:
    """Manages all available skills."""
    
    def __init__(self):
        self.skills: List[Skill] = []
        self._register_default_skills()
        
    def _register_default_skills(self):
        """Register default skills."""
        self.skills.extend([
            GreetingSkill(),
            WeatherSkill(), 
            QuestionAnsweringSkill()
        ])
        
    def register_skill(self, skill: Skill):
        """Register a new skill."""
        self.skills.append(skill)
        
    async def handle_input(self, text: str, context: Optional[Dict[str, Any]] = None) -> SkillResponse:
        """Find appropriate skill and handle input."""
        if context is None:
            context = {}
            
        # Try each skill in order
        for skill in self.skills:
            if skill.can_handle(text, context):
                return await skill.handle(text, context)
                
        # Fallback response
        return SkillResponse(
            text="ይቅርታ፣ ያንን አልተረዳሁም። እባክሽ እንደገና ሞክሪ። Sorry, I didn't understand that. Please try again.",
            speech="ይቅርታ፣ ያንን አልተረዳሁም።"
        )
        
    def list_skills(self) -> List[Dict[str, str]]:
        """List all available skills."""
        return [
            {"name": skill.name, "description": skill.description}
            for skill in self.skills
        ]


# Global skill manager instance
skill_manager = SkillManager()