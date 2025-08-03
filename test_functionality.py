"""Test script to validate new Saba functionality without external dependencies."""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_config():
    """Test configuration loading."""
    print("Testing configuration...")
    try:
        from app.config import config
        print(f"✓ Wake word: {config.wake_word}")
        print(f"✓ Default ASR model: {config.default_asr_model}")
        print(f"✓ Default TTS model: {config.default_tts_model}")
        print(f"✓ Available ASR models: {list(config.asr_models.keys())}")
        print(f"✓ Available TTS models: {list(config.tts_models.keys())}")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

async def test_skills():
    """Test skills framework."""
    print("\nTesting skills framework...")
    try:
        from app.skills import skill_manager, GreetingSkill, WeatherSkill, QuestionAnsweringSkill
        
        # Test skill registration
        print(f"✓ Number of registered skills: {len(skill_manager.skills)}")
        
        # Test greeting skill
        greeting_skill = GreetingSkill()
        assert greeting_skill.can_handle("ሰላም", {})
        assert greeting_skill.can_handle("hello", {})
        response = await greeting_skill.handle("ሰላም", {})
        print(f"✓ Greeting skill response: {response.text[:50]}...")
        
        # Test weather skill
        weather_skill = WeatherSkill()
        assert weather_skill.can_handle("ሰማይ", {})
        assert weather_skill.can_handle("weather", {})
        response = await weather_skill.handle("ሰማይ", {})
        print(f"✓ Weather skill response: {response.text[:50]}...")
        
        # Test Q&A skill
        qa_skill = QuestionAnsweringSkill()
        assert qa_skill.can_handle("ማን ነህ?", {})
        assert qa_skill.can_handle("who are you?", {})
        response = await qa_skill.handle("ማን ነህ?", {})
        print(f"✓ Q&A skill response: {response.text[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Skills test failed: {e}")
        return False

async def test_wake_word():
    """Test wake word detection."""
    print("\nTesting wake word detection...")
    try:
        from app.wake_word import WakeWordDetector, ConversationState, VoiceAssistantCore
        
        # Test wake word detector
        detector = WakeWordDetector()
        assert await detector.detect_in_text("ሰላም ሳባ")
        assert await detector.detect_in_text("hello saba")
        assert not await detector.detect_in_text("hello world")
        print("✓ Wake word detection working")
        
        # Test conversation state
        conversation = ConversationState()
        conversation.start_conversation()
        assert conversation.is_active
        conversation.end_conversation()
        assert not conversation.is_active
        print("✓ Conversation state management working")
        
        # Test voice assistant core
        assistant = VoiceAssistantCore()
        response = await assistant.process_voice_input("ሰላም ሳባ")
        assert response is not None
        print(f"✓ Voice assistant response: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Wake word test failed: {e}")
        return False

async def test_models_config():
    """Test model configuration without loading actual models."""
    print("\nTesting model configurations...")
    try:
        # Test ASR model config
        from app.models.asr import ASRModel
        # We can't actually load the model without dependencies, but we can test the config
        print("✓ ASR model class imported successfully")
        
        # Test TTS model config  
        from app.models.tts import TTSModel
        print("✓ TTS model class imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Model configuration test failed: {e}")
        return False

async def test_controllers():
    """Test controller imports."""
    print("\nTesting controllers...")
    try:
        from app.controllers.voice_controller import router as voice_router
        from app.controllers.asr_controller import router as asr_router
        from app.controllers.tts_controller import router as tts_router
        print("✓ All controllers imported successfully")
        return True
    except Exception as e:
        print(f"✗ Controller test failed: {e}")
        return False

async def run_tests():
    """Run all tests."""
    print("=== Saba Functionality Tests ===\n")
    
    tests = [
        test_config,
        test_skills,
        test_wake_word,
        test_models_config,
        test_controllers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if await test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Saba functionality is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)