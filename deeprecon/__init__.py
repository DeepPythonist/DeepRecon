from .config import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

__version__ = '1.0.0'
__author__ = 'DeepRecon Team'

import json
import os

_current_language = DEFAULT_LANGUAGE
_locale_cache = {}

def set_language(lang: str):
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang
        _load_locale(lang)

def get_message(key_path: str, default: str = '') -> str:
    if _current_language not in _locale_cache:
        _load_locale(_current_language)
    
    keys = key_path.split('.')
    value = _locale_cache.get(_current_language, {})
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, None)
        else:
            return default
    
    return value if value is not None else default

def _load_locale(lang: str):
    locale_path = os.path.join(os.path.dirname(__file__), 'locales', f'{lang}.json')
    try:
        with open(locale_path, 'r', encoding='utf-8') as f:
            _locale_cache[lang] = json.load(f)
    except FileNotFoundError:
        _locale_cache[lang] = {}

set_language(DEFAULT_LANGUAGE)
