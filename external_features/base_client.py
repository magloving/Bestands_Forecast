"""
Base Client für alle External Feature APIs.

Features:
- File-based Caching (Redis optional)
- Rate Limiting
- Retry Logic mit Exponential Backoff
- Automatische Fehlerbehandlung
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class FeatureAPIClient:
    """
    Basis-Klasse für externe Feature APIs.
    
    Implementiert gemeinsame Funktionalität:
    - Caching (Redis/File-based)
    - Rate Limiting
    - Retry Logic
    - Fallback Values
    """
    
    def __init__(self, cache_dir: str = "./cache", cache_ttl_hours: int = 24):
        """
        Initialisiert den API Client.
        
        Args:
            cache_dir: Verzeichnis für File-based Cache
            cache_ttl_hours: Time-to-Live für Cache in Stunden
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.request_count = 0
        self.last_request_time = None
        
    def _get_cache_path(self, key: str) -> Path:
        """Generiert Cache-Pfad für einen Key."""
        # Sanitize key für Filesystem
        safe_key = key.replace('/', '_').replace(':', '_')
        return self.cache_dir / f"{safe_key}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Prüft ob Cache noch gültig ist."""
        if not cache_path.exists():
            return False
        
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - mtime < self.cache_ttl
    
    def _read_cache(self, key: str) -> Optional[Dict]:
        """Liest aus Cache."""
        cache_path = self._get_cache_path(key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Cache read failed: {e}")
                return None
        return None
    
    def _write_cache(self, key: str, data: Dict):
        """Schreibt in Cache."""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Cache write failed: {e}")
    
    def _rate_limit(self, requests_per_minute: int = 60):
        """
        Rate Limiting: Wartet wenn nötig.
        
        Args:
            requests_per_minute: Maximale Requests pro Minute
        """
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            min_interval = 60.0 / requests_per_minute
            
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def _retry_request(self, url: str, max_retries: int = 3, 
                      backoff: float = 2.0, timeout: int = 10) -> Optional[Dict]:
        """
        HTTP Request mit Retry Logic.
        
        Args:
            url: API Endpoint URL
            max_retries: Maximale Anzahl Versuche
            backoff: Exponential Backoff Faktor
            timeout: Request Timeout in Sekunden
            
        Returns:
            JSON Response oder None bei Fehler
        """
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"❌ API Request failed after {max_retries} attempts: {e}")
                    return None
                
                wait_time = backoff ** attempt
                print(f"⚠️  Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
        
        return None
    
    def clear_cache(self):
        """Löscht alle Cache-Dateien."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception as e:
                print(f"⚠️  Failed to delete {cache_file}: {e}")
    
    def get_cache_stats(self) -> Dict:
        """Gibt Cache-Statistiken zurück."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'cache_files': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir),
            'ttl_hours': self.cache_ttl.total_seconds() / 3600
        }
