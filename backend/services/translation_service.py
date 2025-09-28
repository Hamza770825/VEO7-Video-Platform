"""
Translation Service
Handles text translation using deep-translator
"""

import asyncio
from typing import Optional, Dict, List
from deep_translator import GoogleTranslator, MyMemoryTranslator
import langdetect
from functools import lru_cache

class TranslationService:
    def __init__(self):
        """Initialize translation service"""
        self.supported_languages = {
            'ar': 'Arabic',
            'en': 'English', 
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'pl': 'Polish',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'mt': 'Maltese',
            'el': 'Greek',
            'cy': 'Welsh',
            'ga': 'Irish',
            'is': 'Icelandic',
            'mk': 'Macedonian',
            'sq': 'Albanian',
            'bs': 'Bosnian',
            'sr': 'Serbian',
            'me': 'Montenegrin',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'uz': 'Uzbek',
            'tg': 'Tajik',
            'mn': 'Mongolian',
            'ka': 'Georgian',
            'am': 'Amharic',
            'sw': 'Swahili',
            'zu': 'Zulu',
            'af': 'Afrikaans',
            'xh': 'Xhosa',
            'st': 'Sesotho',
            'tn': 'Setswana',
            'ss': 'Siswati',
            've': 'Venda',
            'ts': 'Tsonga',
            'nr': 'Ndebele',
            'nso': 'Northern Sotho'
        }
        
        # Cache for translations
        self._translation_cache = {}
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        try:
            # Check if translation is needed
            if source_lang == target_lang:
                return text
            
            # Check cache first
            cache_key = f"{text}_{source_lang}_{target_lang}"
            if cache_key in self._translation_cache:
                return self._translation_cache[cache_key]
            
            # Validate languages
            if source_lang not in self.supported_languages:
                raise Exception(f"Source language '{source_lang}' not supported")
            
            if target_lang not in self.supported_languages:
                raise Exception(f"Target language '{target_lang}' not supported")
            
            # Perform translation
            translated = await self._perform_translation(text, source_lang, target_lang)
            
            # Cache the result
            self._translation_cache[cache_key] = translated
            
            return translated
            
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    async def _perform_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Perform the actual translation"""
        try:
            # Try Google Translator first
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                result = translator.translate(text)
                if result and result.strip():
                    return result
            except Exception as e:
                print(f"Google Translator failed: {e}")
            
            # Fallback to MyMemory Translator
            try:
                translator = MyMemoryTranslator(source=source_lang, target=target_lang)
                result = translator.translate(text)
                if result and result.strip():
                    return result
            except Exception as e:
                print(f"MyMemory Translator failed: {e}")
            
            # If all translators fail, return original text
            print("All translation services failed, returning original text")
            return text
            
        except Exception as e:
            raise Exception(f"Translation execution failed: {str(e)}")
    
    async def detect_language(self, text: str) -> str:
        """
        Detect the language of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code
        """
        try:
            detected = langdetect.detect(text)
            
            # Map some common detection results
            lang_mapping = {
                'zh-cn': 'zh',
                'zh-tw': 'zh',
                'pt-br': 'pt',
                'pt-pt': 'pt'
            }
            
            detected = lang_mapping.get(detected, detected)
            
            # Validate detected language
            if detected in self.supported_languages:
                return detected
            else:
                # Default to English if detection fails
                return 'en'
                
        except Exception as e:
            print(f"Language detection failed: {e}")
            return 'en'  # Default to English
    
    async def get_language_confidence(self, text: str) -> Dict[str, float]:
        """
        Get language detection confidence scores
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of language codes and confidence scores
        """
        try:
            from langdetect import detect_langs
            
            detected_langs = detect_langs(text)
            confidence_scores = {}
            
            for lang_prob in detected_langs:
                lang_code = str(lang_prob.lang)
                confidence = lang_prob.prob
                
                # Map language codes
                lang_mapping = {
                    'zh-cn': 'zh',
                    'zh-tw': 'zh',
                    'pt-br': 'pt',
                    'pt-pt': 'pt'
                }
                
                lang_code = lang_mapping.get(lang_code, lang_code)
                
                if lang_code in self.supported_languages:
                    confidence_scores[lang_code] = confidence
            
            return confidence_scores
            
        except Exception as e:
            print(f"Language confidence detection failed: {e}")
            return {'en': 1.0}  # Default to English with full confidence
    
    async def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        """
        Translate multiple texts in batch
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated texts
        """
        try:
            translated_texts = []
            
            for text in texts:
                translated = await self.translate_text(text, source_lang, target_lang)
                translated_texts.append(translated)
            
            return translated_texts
            
        except Exception as e:
            raise Exception(f"Batch translation failed: {str(e)}")
    
    async def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()
    
    async def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.supported_languages
    
    async def get_language_name(self, lang_code: str) -> str:
        """Get language name from code"""
        return self.supported_languages.get(lang_code, "Unknown")
    
    @lru_cache(maxsize=1000)
    def _cached_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Cached translation for frequently used phrases"""
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(text)
        except:
            return text
    
    async def translate_with_alternatives(self, text: str, source_lang: str, target_lang: str) -> Dict[str, str]:
        """
        Get translation with alternative options
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Dictionary with main translation and alternatives
        """
        try:
            results = {}
            
            # Main translation (Google)
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                results['google'] = translator.translate(text)
            except:
                results['google'] = text
            
            # Alternative translation (MyMemory)
            try:
                translator = MyMemoryTranslator(source=source_lang, target=target_lang)
                results['mymemory'] = translator.translate(text)
            except:
                results['mymemory'] = text
            
            # Select best translation (prefer Google if available)
            main_translation = results.get('google', results.get('mymemory', text))
            
            return {
                'main': main_translation,
                'alternatives': results
            }
            
        except Exception as e:
            raise Exception(f"Alternative translation failed: {str(e)}")
    
    def clear_cache(self):
        """Clear translation cache"""
        self._translation_cache.clear()
    
    def get_cache_size(self) -> int:
        """Get current cache size"""
        return len(self._translation_cache)

# Common phrases for quick translation
COMMON_PHRASES = {
    'welcome': {
        'en': 'Welcome',
        'ar': 'مرحباً',
        'fr': 'Bienvenue',
        'es': 'Bienvenido',
        'de': 'Willkommen',
        'it': 'Benvenuto',
        'pt': 'Bem-vindo',
        'ru': 'Добро пожаловать',
        'ja': 'ようこそ',
        'ko': '환영합니다',
        'zh': '欢迎',
        'hi': 'स्वागत है',
        'tr': 'Hoş geldiniz'
    },
    'thank_you': {
        'en': 'Thank you',
        'ar': 'شكراً لك',
        'fr': 'Merci',
        'es': 'Gracias',
        'de': 'Danke',
        'it': 'Grazie',
        'pt': 'Obrigado',
        'ru': 'Спасибо',
        'ja': 'ありがとう',
        'ko': '감사합니다',
        'zh': '谢谢',
        'hi': 'धन्यवाद',
        'tr': 'Teşekkür ederim'
    },
    'processing': {
        'en': 'Processing...',
        'ar': 'جاري المعالجة...',
        'fr': 'Traitement en cours...',
        'es': 'Procesando...',
        'de': 'Verarbeitung...',
        'it': 'Elaborazione...',
        'pt': 'Processando...',
        'ru': 'Обработка...',
        'ja': '処理中...',
        'ko': '처리 중...',
        'zh': '处理中...',
        'hi': 'प्रसंस्करण...',
        'tr': 'İşleniyor...'
    }
}


"""
Enhanced Translation Service
Handles text translation with advanced caching and improved accuracy
"""

import asyncio
import os
import json
import hashlib
import time
from typing import Optional, Dict, List, Tuple
from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
import langdetect
from functools import lru_cache
from datetime import datetime, timedelta

class EnhancedTranslationService:
    def __init__(self, cache_dir: str = "cache/translation"):
        """Initialize enhanced translation service with persistent caching"""
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.supported_languages = {
            'ar': 'Arabic',
            'en': 'English', 
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'pl': 'Polish',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'hr': 'Croatian',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'mt': 'Maltese',
            'el': 'Greek',
            'cy': 'Welsh',
            'ga': 'Irish',
            'is': 'Icelandic',
            'mk': 'Macedonian',
            'sq': 'Albanian',
            'bs': 'Bosnian',
            'sr': 'Serbian',
            'me': 'Montenegrin',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'kk': 'Kazakh',
            'ky': 'Kyrgyz',
            'uz': 'Uzbek',
            'tg': 'Tajik',
            'mn': 'Mongolian',
            'ka': 'Georgian',
            'am': 'Amharic',
            'sw': 'Swahili',
            'zu': 'Zulu',
            'af': 'Afrikaans',
            'xh': 'Xhosa',
            'st': 'Sesotho',
            'tn': 'Setswana',
            'ss': 'Siswati',
            've': 'Venda',
            'ts': 'Tsonga',
            'nr': 'Ndebele',
            'nso': 'Northern Sotho'
        }
        
        # Enhanced caching system
        self._memory_cache = {}  # In-memory cache for fast access
        self._persistent_cache = {}  # Persistent cache loaded from disk
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'total_translations': 0
        }
        
        # Translation quality settings
        self.quality_settings = {
            'high': {
                'use_multiple_services': True,
                'confidence_threshold': 0.8,
                'retry_attempts': 3
            },
            'medium': {
                'use_multiple_services': True,
                'confidence_threshold': 0.6,
                'retry_attempts': 2
            },
            'fast': {
                'use_multiple_services': False,
                'confidence_threshold': 0.4,
                'retry_attempts': 1
            }
        }
        
        # Load persistent cache
        self._load_persistent_cache()
    
    def _load_persistent_cache(self):
        """Load persistent cache from disk"""
        cache_file = os.path.join(self.cache_dir, "translation_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self._persistent_cache = json.load(f)
                print(f"Loaded {len(self._persistent_cache)} cached translations")
            except Exception as e:
                print(f"Failed to load cache: {e}")
                self._persistent_cache = {}
    
    def _save_persistent_cache(self):
        """Save persistent cache to disk"""
        cache_file = os.path.join(self.cache_dir, "translation_cache.json")
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._persistent_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save cache: {e}")
    
    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate cache key for translation"""
        content = f"{text.strip().lower()}_{source_lang}_{target_lang}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str, 
                           quality: str = "medium") -> Dict[str, any]:
        """
        Enhanced translation with quality settings and detailed results
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            quality: Translation quality (high, medium, fast)
            
        Returns:
            Dictionary with translation results and metadata
        """
        try:
            start_time = time.time()
            
            # Check if translation is needed
            if source_lang == target_lang:
                return {
                    'translated_text': text,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'confidence': 1.0,
                    'processing_time': 0.0,
                    'cache_hit': False,
                    'quality': quality
                }
            
            # Validate languages
            if source_lang not in self.supported_languages:
                raise Exception(f"Source language '{source_lang}' not supported")
            
            if target_lang not in self.supported_languages:
                raise Exception(f"Target language '{target_lang}' not supported")
            
            # Check cache
            cache_key = self._get_cache_key(text, source_lang, target_lang)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                self._cache_stats['hits'] += 1
                processing_time = time.time() - start_time
                cached_result.update({
                    'processing_time': processing_time,
                    'cache_hit': True
                })
                return cached_result
            
            # Perform translation
            self._cache_stats['misses'] += 1
            self._cache_stats['total_translations'] += 1
            
            quality_config = self.quality_settings.get(quality, self.quality_settings['medium'])
            
            if quality_config['use_multiple_services']:
                result = await self._translate_with_multiple_services(
                    text, source_lang, target_lang, quality_config
                )
            else:
                result = await self._translate_single_service(
                    text, source_lang, target_lang, quality_config
                )
            
            processing_time = time.time() - start_time
            
            # Prepare final result
            final_result = {
                'translated_text': result['text'],
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': result['confidence'],
                'processing_time': processing_time,
                'cache_hit': False,
                'quality': quality,
                'service_used': result.get('service', 'unknown')
            }
            
            # Cache the result
            self._save_to_cache(cache_key, final_result)
            
            return final_result
            
        except Exception as e:
            raise Exception(f"Enhanced translation failed: {str(e)}")
    
    async def _translate_with_multiple_services(self, text: str, source_lang: str, 
                                              target_lang: str, quality_config: Dict) -> Dict:
        """Translate using multiple services for better accuracy"""
        results = []
        services = [
            ('google', GoogleTranslator),
            ('mymemory', MyMemoryTranslator)
        ]
        
        for service_name, service_class in services:
            try:
                translator = service_class(source=source_lang, target=target_lang)
                translated = translator.translate(text)
                
                if translated and translated.strip():
                    confidence = await self._calculate_confidence(text, translated, source_lang, target_lang)
                    results.append({
                        'text': translated,
                        'confidence': confidence,
                        'service': service_name
                    })
            except Exception as e:
                print(f"{service_name} translation failed: {e}")
                continue
        
        if not results:
            return {'text': text, 'confidence': 0.0, 'service': 'none'}
        
        # Select best result based on confidence
        best_result = max(results, key=lambda x: x['confidence'])
        
        # If confidence is too low, try to improve
        if best_result['confidence'] < quality_config['confidence_threshold']:
            improved_result = await self._improve_translation(text, source_lang, target_lang, results)
            if improved_result:
                return improved_result
        
        return best_result
    
    async def _translate_single_service(self, text: str, source_lang: str, 
                                      target_lang: str, quality_config: Dict) -> Dict:
        """Translate using single service for speed"""
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            if translated and translated.strip():
                confidence = await self._calculate_confidence(text, translated, source_lang, target_lang)
                return {
                    'text': translated,
                    'confidence': confidence,
                    'service': 'google'
                }
        except Exception as e:
            print(f"Google translation failed: {e}")
        
        # Fallback to MyMemory
        try:
            translator = MyMemoryTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            
            if translated and translated.strip():
                confidence = await self._calculate_confidence(text, translated, source_lang, target_lang)
                return {
                    'text': translated,
                    'confidence': confidence,
                    'service': 'mymemory'
                }
        except Exception as e:
            print(f"MyMemory translation failed: {e}")
        
        return {'text': text, 'confidence': 0.0, 'service': 'none'}
    
    async def _calculate_confidence(self, original: str, translated: str, 
                                  source_lang: str, target_lang: str) -> float:
        """Calculate translation confidence score"""
        try:
            # Basic confidence calculation based on various factors
            confidence = 0.5  # Base confidence
            
            # Length similarity (translations shouldn't be too different in length)
            length_ratio = min(len(translated), len(original)) / max(len(translated), len(original))
            confidence += length_ratio * 0.2
            
            # Check if translation is not empty or same as original
            if translated.strip() and translated.strip() != original.strip():
                confidence += 0.2
            
            # Language detection on result
            try:
                detected_lang = langdetect.detect(translated)
                if detected_lang == target_lang:
                    confidence += 0.1
            except:
                pass
            
            return min(confidence, 1.0)
            
        except Exception as e:
            print(f"Confidence calculation failed: {e}")
            return 0.5
    
    async def _improve_translation(self, text: str, source_lang: str, target_lang: str, 
                                 existing_results: List[Dict]) -> Optional[Dict]:
        """Attempt to improve translation quality"""
        try:
            # Try breaking text into smaller chunks for better translation
            if len(text) > 100:
                sentences = text.split('. ')
                if len(sentences) > 1:
                    translated_sentences = []
                    total_confidence = 0
                    
                    for sentence in sentences:
                        if sentence.strip():
                            sentence_result = await self._translate_single_service(
                                sentence.strip() + '.', source_lang, target_lang, {}
                            )
                            translated_sentences.append(sentence_result['text'])
                            total_confidence += sentence_result['confidence']
                    
                    if translated_sentences:
                        improved_text = ' '.join(translated_sentences)
                        avg_confidence = total_confidence / len(translated_sentences)
                        
                        return {
                            'text': improved_text,
                            'confidence': avg_confidence,
                            'service': 'chunked'
                        }
            
            return None
            
        except Exception as e:
            print(f"Translation improvement failed: {e}")
            return None
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get translation from cache"""
        # Check memory cache first
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]
        
        # Check persistent cache
        if cache_key in self._persistent_cache:
            result = self._persistent_cache[cache_key]
            # Move to memory cache for faster access
            self._memory_cache[cache_key] = result
            return result
        
        return None
    
    def _save_to_cache(self, cache_key: str, result: Dict):
        """Save translation to cache"""
        # Remove cache_hit and processing_time for storage
        cache_result = {k: v for k, v in result.items() 
                       if k not in ['cache_hit', 'processing_time']}
        
        # Save to memory cache
        self._memory_cache[cache_key] = cache_result
        
        # Save to persistent cache
        self._persistent_cache[cache_key] = cache_result
        
        # Periodically save to disk
        if len(self._persistent_cache) % 10 == 0:
            self._save_persistent_cache()
    
    async def detect_language_enhanced(self, text: str) -> Dict[str, any]:
        """Enhanced language detection with confidence scores"""
        try:
            # Get multiple detection results
            detected_langs = langdetect.detect_langs(text)
            
            results = []
            for lang_prob in detected_langs:
                lang_code = str(lang_prob.lang)
                confidence = lang_prob.prob
                
                # Map language codes
                lang_mapping = {
                    'zh-cn': 'zh',
                    'zh-tw': 'zh',
                    'pt-br': 'pt',
                    'pt-pt': 'pt'
                }
                
                lang_code = lang_mapping.get(lang_code, lang_code)
                
                if lang_code in self.supported_languages:
                    results.append({
                        'language': lang_code,
                        'language_name': self.supported_languages[lang_code],
                        'confidence': confidence
                    })
            
            # Sort by confidence
            results.sort(key=lambda x: x['confidence'], reverse=True)
            
            return {
                'primary_language': results[0] if results else {'language': 'en', 'language_name': 'English', 'confidence': 1.0},
                'all_detections': results,
                'text_length': len(text),
                'detection_time': time.time()
            }
            
        except Exception as e:
            print(f"Enhanced language detection failed: {e}")
            return {
                'primary_language': {'language': 'en', 'language_name': 'English', 'confidence': 1.0},
                'all_detections': [],
                'text_length': len(text),
                'detection_time': time.time()
            }
    
    async def translate_batch_enhanced(self, texts: List[str], source_lang: str, 
                                     target_lang: str, quality: str = "medium") -> List[Dict]:
        """Enhanced batch translation with progress tracking"""
        try:
            results = []
            total_texts = len(texts)
            
            for i, text in enumerate(texts):
                try:
                    result = await self.translate_text(text, source_lang, target_lang, quality)
                    result['batch_index'] = i
                    result['batch_progress'] = (i + 1) / total_texts
                    results.append(result)
                except Exception as e:
                    # Add error result
                    results.append({
                        'translated_text': text,
                        'source_language': source_lang,
                        'target_language': target_lang,
                        'confidence': 0.0,
                        'processing_time': 0.0,
                        'cache_hit': False,
                        'quality': quality,
                        'batch_index': i,
                        'batch_progress': (i + 1) / total_texts,
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            raise Exception(f"Enhanced batch translation failed: {str(e)}")
    
    async def get_translation_stats(self) -> Dict[str, any]:
        """Get translation service statistics"""
        cache_hit_rate = 0
        if self._cache_stats['total_translations'] > 0:
            cache_hit_rate = self._cache_stats['hits'] / (self._cache_stats['hits'] + self._cache_stats['misses'])
        
        return {
            'total_translations': self._cache_stats['total_translations'],
            'cache_hits': self._cache_stats['hits'],
            'cache_misses': self._cache_stats['misses'],
            'cache_hit_rate': cache_hit_rate,
            'memory_cache_size': len(self._memory_cache),
            'persistent_cache_size': len(self._persistent_cache),
            'supported_languages_count': len(self.supported_languages)
        }
    
    async def optimize_cache(self):
        """Optimize cache by removing old or low-confidence entries"""
        try:
            # Remove low-confidence translations from persistent cache
            to_remove = []
            for key, value in self._persistent_cache.items():
                if value.get('confidence', 0) < 0.3:
                    to_remove.append(key)
            
            for key in to_remove:
                del self._persistent_cache[key]
            
            # Clear memory cache if it gets too large
            if len(self._memory_cache) > 1000:
                self._memory_cache.clear()
            
            # Save optimized cache
            self._save_persistent_cache()
            
            print(f"Cache optimized: removed {len(to_remove)} low-confidence entries")
            
        except Exception as e:
            print(f"Cache optimization failed: {e}")
    
    def clear_all_caches(self):
        """Clear all caches"""
        self._memory_cache.clear()
        self._persistent_cache.clear()
        self._save_persistent_cache()
        print("All caches cleared")

# Backward compatibility
TranslationService = EnhancedTranslationService

COMMON_PHRASES = {
    'welcome': {
        'en': 'Welcome',
        'ar': 'مرحباً',
        'fr': 'Bienvenue',
        'es': 'Bienvenido',
        'de': 'Willkommen',
        'it': 'Benvenuto',
        'pt': 'Bem-vindo',
        'ru': 'Добро пожаловать',
        'ja': 'ようこそ',
        'ko': '환영합니다',
        'zh': '欢迎',
        'hi': 'स्वागत है',
        'tr': 'Hoş geldiniz'
    },
    'thank_you': {
        'en': 'Thank you',
        'ar': 'شكراً لك',
        'fr': 'Merci',
        'es': 'Gracias',
        'de': 'Danke',
        'it': 'Grazie',
        'pt': 'Obrigado',
        'ru': 'Спасибо',
        'ja': 'ありがとう',
        'ko': '감사합니다',
        'zh': '谢谢',
        'hi': 'धन्यवाद',
        'tr': 'Teşekkür ederim'
    },
    'processing': {
        'en': 'Processing...',
        'ar': 'جاري المعالجة...',
        'fr': 'Traitement en cours...',
        'es': 'Procesando...',
        'de': 'Verarbeitung...',
        'it': 'Elaborazione...',
        'pt': 'Processando...',
        'ru': 'Обработка...',
        'ja': '処理中...',
        'ko': '처리 중...',
        'zh': '处理中...',
        'hi': 'प्रसंस्करण...',
        'tr': 'İşleniyor...'
    }
}