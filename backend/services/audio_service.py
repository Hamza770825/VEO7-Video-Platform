"""Enhanced Audio Service
Handles text-to-speech conversion with multiple voice options and quality settings
"""

import os
import asyncio
import tempfile
import aiohttp
import hashlib
from typing import Optional, Dict, List
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import pyttsx3
from functools import lru_cache
import json

# Audio quality presets
AUDIO_QUALITY_PRESETS = {
    "low": {
        "sample_rate": 16000,
        "bitrate": "64k",
        "channels": 1
    },
    "medium": {
        "sample_rate": 22050,
        "bitrate": "128k",
        "channels": 1
    },
    "high": {
        "sample_rate": 44100,
        "bitrate": "192k",
        "channels": 2
    },
    "ultra": {
        "sample_rate": 48000,
        "bitrate": "320k",
        "channels": 2
    }
}

class AudioService:
    def __init__(self, temp_dir: str = "temp", cache_dir: str = "cache/audio"):
        """Initialize enhanced audio service"""
        self.temp_dir = temp_dir
        self.cache_dir = cache_dir
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize offline TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
            self._configure_offline_voices()
        except:
            self.tts_engine = None
            print("Warning: pyttsx3 not available, using gTTS only")
        
        # Audio cache for frequently used phrases
        self.audio_cache = {}
        self._load_cache_index()
    
    def _configure_offline_voices(self):
        """Configure offline TTS voices"""
        if not self.tts_engine:
            return
        
        voices = self.tts_engine.getProperty('voices')
        self.offline_voices = {}
        
        for voice in voices:
            # Categorize voices by language and gender
            voice_id = voice.id.lower()
            voice_name = voice.name.lower()
            
            # Detect language
            lang = "en"  # default
            if any(x in voice_name for x in ["arabic", "عربي"]):
                lang = "ar"
            elif any(x in voice_name for x in ["french", "français"]):
                lang = "fr"
            elif any(x in voice_name for x in ["spanish", "español"]):
                lang = "es"
            elif any(x in voice_name for x in ["german", "deutsch"]):
                lang = "de"
            
            # Detect gender
            gender = "male"  # default
            if any(x in voice_name for x in ["female", "woman", "lady", "زينب", "فاطمة"]):
                gender = "female"
            
            if lang not in self.offline_voices:
                self.offline_voices[lang] = {}
            
            self.offline_voices[lang][gender] = voice.id
    
    def _load_cache_index(self):
        """Load audio cache index"""
        cache_index_path = os.path.join(self.cache_dir, "cache_index.json")
        if os.path.exists(cache_index_path):
            try:
                with open(cache_index_path, 'r', encoding='utf-8') as f:
                    self.audio_cache = json.load(f)
            except:
                self.audio_cache = {}
    
    def _save_cache_index(self):
        """Save audio cache index"""
        cache_index_path = os.path.join(self.cache_dir, "cache_index.json")
        try:
            with open(cache_index_path, 'w', encoding='utf-8') as f:
                json.dump(self.audio_cache, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _get_cache_key(self, text: str, language: str, voice: str, speed: float, quality: str) -> str:
        """Generate cache key for audio"""
        content = f"{text}_{language}_{voice}_{speed}_{quality}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    async def generate_audio(self, text: str, language: str = "ar", 
                           voice: str = "female", speed: float = 1.0, 
                           quality: str = "high", output_path: str = None) -> str:
        """
        Generate enhanced audio from text with multiple voice options
        
        Args:
            text: Text to convert to speech
            language: Language code (ar, en, fr, etc.)
            voice: Voice type (male, female, child)
            speed: Speech speed multiplier
            quality: Audio quality (low, medium, high, ultra)
            output_path: Output file path
            
        Returns:
            Path to generated audio file
        """
        # Validate inputs
        if language not in SUPPORTED_LANGUAGES:
            raise Exception(f"Language '{language}' not supported")
        
        available_voices = SUPPORTED_LANGUAGES[language]["voices"]
        if voice not in available_voices:
            voice = "female" if "female" in available_voices else list(available_voices.keys())[0]
        
        if quality not in AUDIO_QUALITY_PRESETS:
            quality = "high"
        
        # Check cache first
        cache_key = self._get_cache_key(text, language, voice, speed, quality)
        cached_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        
        if os.path.exists(cached_path):
            if output_path and output_path != cached_path:
                # Copy cached file to desired output path
                import shutil
                shutil.copy2(cached_path, output_path)
                return output_path
            return cached_path
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"audio_{cache_key}.wav")
        
        try:
            # Use gTTS for online generation (better quality)
            if await self._is_internet_available():
                audio_path = await self._generate_with_gtts_enhanced(text, language, voice, quality, output_path)
            else:
                # Fallback to offline TTS
                audio_path = await self._generate_with_pyttsx3_enhanced(text, language, voice, quality, output_path)
            
            # Adjust speed if needed
            if speed != 1.0:
                audio_path = await self._adjust_speed(audio_path, speed)
            
            # Apply quality settings
            audio_path = await self._apply_quality_settings(audio_path, quality)
            
            # Cache the result
            if audio_path != cached_path:
                import shutil
                shutil.copy2(audio_path, cached_path)
                self.audio_cache[cache_key] = {
                    "text": text,
                    "language": language,
                    "voice": voice,
                    "speed": speed,
                    "quality": quality,
                    "created_at": asyncio.get_event_loop().time()
                }
                self._save_cache_index()
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Audio generation failed: {str(e)}")
    
    async def get_available_voices(self, language: str = None) -> Dict:
        """
        Get available voices for a language or all languages
        
        Args:
            language: Language code (optional)
            
        Returns:
            Dictionary of available voices
        """
        if language:
            if language in SUPPORTED_LANGUAGES:
                return {language: SUPPORTED_LANGUAGES[language]}
            else:
                return {}
        
        return SUPPORTED_LANGUAGES
    
    async def estimate_audio_duration(self, text: str, language: str = "ar", 
                                    voice: str = "female", speed: float = 1.0) -> float:
        """
        Estimate audio duration based on text length and language
        
        Args:
            text: Text to analyze
            language: Language code
            voice: Voice type
            speed: Speech speed multiplier
            
        Returns:
            Estimated duration in seconds
        """
        # Average speaking rates (words per minute) by language
        speaking_rates = {
            "ar": 140,  # Arabic
            "en": 160,  # English
            "fr": 150,  # French
            "es": 155,  # Spanish
            "de": 145,  # German
            "it": 150,  # Italian
            "pt": 155,  # Portuguese
            "ru": 140,  # Russian
            "ja": 130,  # Japanese
            "ko": 135,  # Korean
            "zh": 125,  # Chinese
            "hi": 145,  # Hindi
            "tr": 150   # Turkish
        }
        
        # Estimate word count (rough approximation)
        word_count = len(text.split())
        if language in ["ar", "zh", "ja", "ko"]:
            # For languages without clear word boundaries
            word_count = len(text) / 3  # Rough character-to-word ratio
        
        base_rate = speaking_rates.get(language, 150)
        
        # Adjust for voice type
        if voice == "child":
            base_rate *= 0.9  # Children speak slightly slower
        elif voice == "male":
            base_rate *= 1.05  # Males might speak slightly faster
        
        # Calculate duration
        duration = (word_count / base_rate) * 60  # Convert to seconds
        
        # Adjust for speed
        duration = duration / speed
        
        # Add padding for natural pauses
        duration *= 1.1
        
        return max(duration, 1.0)  # Minimum 1 second
    
    async def _generate_with_gtts_enhanced(self, text: str, language: str, voice: str, 
                                          quality: str, output_path: str) -> str:
        """Generate enhanced audio using Google Text-to-Speech"""
        try:
            # Get language configuration
            lang_config = SUPPORTED_LANGUAGES[language]["voices"][voice]
            gtts_lang = lang_config["gtts"]
            
            # Generate TTS with voice-specific settings
            slow_speech = voice == "child"  # Children speak slower
            
            tts = gTTS(text=text, lang=gtts_lang, slow=slow_speech)
            
            # Save to temporary mp3 file
            temp_mp3 = output_path.replace(".wav", ".mp3")
            tts.save(temp_mp3)
            
            # Convert to WAV with quality settings
            audio = AudioSegment.from_mp3(temp_mp3)
            
            # Apply voice-specific modifications
            if voice == "male":
                # Lower pitch for male voice
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * 0.9)
                }).set_frame_rate(audio.frame_rate)
            elif voice == "child":
                # Higher pitch for child voice
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * 1.2)
                }).set_frame_rate(audio.frame_rate)
            
            # Export with quality settings
            quality_preset = AUDIO_QUALITY_PRESETS[quality]
            audio = audio.set_frame_rate(quality_preset["sample_rate"])
            audio = audio.set_channels(quality_preset["channels"])
            
            audio.export(output_path, format="wav", bitrate=quality_preset["bitrate"])
            
            # Clean up temp file
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Enhanced gTTS generation failed: {str(e)}")
    
    async def _generate_with_gtts(self, text: str, language: str, output_path: str) -> str:
        """Generate audio using Google Text-to-Speech (legacy method)"""
        return await self._generate_with_gtts_enhanced(text, language, "female", "high", output_path)
    
    async def _generate_with_pyttsx3_enhanced(self, text: str, language: str, voice: str, 
                                             quality: str, output_path: str) -> str:
        """Generate enhanced audio using pyttsx3 (offline)"""
        try:
            if not self.tts_engine:
                raise Exception("Offline TTS engine not available")
            
            # Set voice based on language and gender
            if hasattr(self, 'offline_voices') and language in self.offline_voices:
                if voice in self.offline_voices[language]:
                    self.tts_engine.setProperty('voice', self.offline_voices[language][voice])
                else:
                    # Fallback to any available voice for the language
                    available_voices = list(self.offline_voices[language].values())
                    if available_voices:
                        self.tts_engine.setProperty('voice', available_voices[0])
            
            # Set speech rate based on voice type
            base_rate = 150
            if voice == "child":
                base_rate = 130  # Slower for child voice
            elif voice == "male":
                base_rate = 160  # Slightly faster for male voice
            
            self.tts_engine.setProperty('rate', base_rate)
            
            # Set volume
            self.tts_engine.setProperty('volume', 0.9)
            
            # Generate speech to temporary file
            temp_output = output_path.replace('.wav', '_temp.wav')
            self.tts_engine.save_to_file(text, temp_output)
            self.tts_engine.runAndWait()
            
            # Apply quality settings using pydub
            if os.path.exists(temp_output):
                audio = AudioSegment.from_wav(temp_output)
                
                # Apply voice modifications
                if voice == "male":
                    # Lower pitch for male voice
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 0.85)
                    }).set_frame_rate(audio.frame_rate)
                elif voice == "child":
                    # Higher pitch for child voice
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 1.3)
                    }).set_frame_rate(audio.frame_rate)
                
                # Apply quality settings
                quality_preset = AUDIO_QUALITY_PRESETS[quality]
                audio = audio.set_frame_rate(quality_preset["sample_rate"])
                audio = audio.set_channels(quality_preset["channels"])
                
                audio.export(output_path, format="wav", bitrate=quality_preset["bitrate"])
                
                # Clean up temp file
                os.remove(temp_output)
            else:
                raise Exception("Failed to generate temporary audio file")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Enhanced pyttsx3 generation failed: {str(e)}")
    
    async def _generate_with_pyttsx3(self, text: str, output_path: str) -> str:
        """Generate audio using pyttsx3 (offline) - legacy method"""
        return await self._generate_with_pyttsx3_enhanced(text, "en", "female", "high", output_path)
    
    async def _apply_quality_settings(self, audio_path: str, quality: str) -> str:
        """Apply quality settings to audio file"""
        try:
            if quality == "high":  # Already applied during generation
                return audio_path
            
            # Load audio
            audio = AudioSegment.from_wav(audio_path)
            
            # Apply quality preset
            quality_preset = AUDIO_QUALITY_PRESETS[quality]
            audio = audio.set_frame_rate(quality_preset["sample_rate"])
            audio = audio.set_channels(quality_preset["channels"])
            
            # Create output path for quality-adjusted file
            quality_path = audio_path.replace('.wav', f'_{quality}.wav')
            audio.export(quality_path, format="wav", bitrate=quality_preset["bitrate"])
            
            # Replace original file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            os.rename(quality_path, audio_path)
            
            return audio_path
            
        except Exception as e:
            print(f"Quality adjustment failed: {e}")
            return audio_path  # Return original if quality adjustment fails
    
    async def _adjust_speed(self, audio_path: str, speed: float) -> str:
        """Adjust audio playback speed"""
        try:
            # Load audio
            audio = AudioSegment.from_wav(audio_path)
            
            # Adjust speed
            if speed > 1.0:
                # Speed up
                audio = speedup(audio, playback_speed=speed)
            elif speed < 1.0:
                # Slow down
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * speed)
                }).set_frame_rate(audio.frame_rate)
            
            # Save adjusted audio
            adjusted_path = audio_path.replace(".wav", f"_speed_{speed}.wav")
            audio.export(adjusted_path, format="wav")
            
            # Replace original file
            os.remove(audio_path)
            os.rename(adjusted_path, audio_path)
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Speed adjustment failed: {str(e)}")
    
    async def _is_internet_available(self) -> bool:
        """Check if internet connection is available"""
        try:
            import urllib.request
            urllib.request.urlopen('http://www.google.com', timeout=3)
            return True
        except:
            return False
    
    async def get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio = AudioSegment.from_wav(audio_path)
            return len(audio) / 1000.0  # Convert to seconds
        except Exception as e:
            raise Exception(f"Duration calculation failed: {str(e)}")
    
    async def enhance_audio(self, audio_path: str) -> str:
        """Enhance audio quality"""
        try:
            audio = AudioSegment.from_wav(audio_path)
            
            # Normalize audio
            normalized = audio.normalize()
            
            # Apply gentle compression
            compressed = normalized.compress_dynamic_range(threshold=-20.0, ratio=4.0)
            
            # Save enhanced audio
            enhanced_path = audio_path.replace(".wav", "_enhanced.wav")
            compressed.export(enhanced_path, format="wav")
            
            # Replace original
            os.remove(audio_path)
            os.rename(enhanced_path, audio_path)
            
            return audio_path
            
        except Exception as e:
            print(f"Audio enhancement failed: {str(e)}")
            return audio_path  # Return original if enhancement fails
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file in os.listdir(self.temp_dir):
                if file.endswith(('.wav', '.mp3', '.tmp')):
                    file_path = os.path.join(self.temp_dir, file)
                    # Remove files older than 1 hour
                    if os.path.getctime(file_path) < (time.time() - 3600):
                        os.remove(file_path)
        except Exception as e:
            print(f"Cleanup failed: {str(e)}")

# Language support configuration with voice options
SUPPORTED_LANGUAGES = {
    "ar": {
        "name": "Arabic",
        "voices": {
            "male": {"gtts": "ar", "quality": "high"},
            "female": {"gtts": "ar", "quality": "high"},
            "child": {"gtts": "ar", "quality": "medium"}
        }
    },
    "en": {
        "name": "English", 
        "voices": {
            "male": {"gtts": "en", "quality": "high"},
            "female": {"gtts": "en", "quality": "high"},
            "child": {"gtts": "en", "quality": "medium"}
        }
    },
    "fr": {
        "name": "French",
        "voices": {
            "male": {"gtts": "fr", "quality": "high"},
            "female": {"gtts": "fr", "quality": "high"}
        }
    },
    "es": {
        "name": "Spanish",
        "voices": {
            "male": {"gtts": "es", "quality": "high"},
            "female": {"gtts": "es", "quality": "high"}
        }
    },
    "de": {
        "name": "German",
        "voices": {
            "male": {"gtts": "de", "quality": "high"},
            "female": {"gtts": "de", "quality": "high"}
        }
    },
    "it": {
        "name": "Italian",
        "voices": {
            "male": {"gtts": "it", "quality": "high"},
            "female": {"gtts": "it", "quality": "high"}
        }
    },
    "pt": {
        "name": "Portuguese",
        "voices": {
            "male": {"gtts": "pt", "quality": "high"},
            "female": {"gtts": "pt", "quality": "high"}
        }
    },
    "ru": {
        "name": "Russian",
        "voices": {
            "male": {"gtts": "ru", "quality": "high"},
            "female": {"gtts": "ru", "quality": "high"}
        }
    },
    "ja": {
        "name": "Japanese",
        "voices": {
            "male": {"gtts": "ja", "quality": "high"},
            "female": {"gtts": "ja", "quality": "high"}
        }
    },
    "ko": {
        "name": "Korean",
        "voices": {
            "male": {"gtts": "ko", "quality": "high"},
            "female": {"gtts": "ko", "quality": "high"}
        }
    },
    "zh": {
        "name": "Chinese",
        "voices": {
            "male": {"gtts": "zh", "quality": "high"},
            "female": {"gtts": "zh", "quality": "high"}
        }
    },
    "hi": {
        "name": "Hindi",
        "voices": {
            "male": {"gtts": "hi", "quality": "high"},
            "female": {"gtts": "hi", "quality": "high"}
        }
    },
    "tr": {
        "name": "Turkish",
        "voices": {
            "male": {"gtts": "tr", "quality": "high"},
            "female": {"gtts": "tr", "quality": "high"}
        }
    }
}