import os
from google import genai
from google.genai import types
from app import redis_client
import logging

logger = logging.getLogger(__name__)

class GeminiSummarizer:
    """Generate earthquake summaries using Gemini AI"""
    
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = (
            "You are an AI assistant that summarizes PHIVOLCS earthquake reports. "
            "Your tone should be calm, and formal but still easy-to-digest — as if you're explaining the situation to everyday Filipinos. "
            "Avoid technical jargon, but keep the facts accurate. Avoid greetings as well -- just straight to the report. "
            "Never use decorations (like bold, italics, headers, or bullets). "
            "Respond in plain text only."
        )
    
    def create_summary(self, earthquake_data, include_safety_tips=True):
        """Generate earthquake summary"""
        
        magnitude_float = self._parse_magnitude(earthquake_data['magnitude'])
        
        magnitude_condition = ""
        if magnitude_float >= 4.0 and include_safety_tips:
            magnitude_condition = (
                "Since the magnitude is 4.0 or higher, "
                "include 2 short, simple, and relevant safety tips for the affected areas. "
            )
        
        contents = (
            "TASK:\n"
            "Summarize the following earthquake information in exactly 5 sentences. "
            "Make it easy to understand and reassuring in tone. "
            f"{magnitude_condition}\n\n"
            "EARTHQUAKE DETAILS:\n"
            f"- Date and Time: {earthquake_data['date_time']}\n"
            f"- Latitude: {earthquake_data['latitude']}\n"
            f"- Longitude: {earthquake_data['longitude']}\n"
            f"- Depth: {earthquake_data['depth']}\n"
            f"- Magnitude: {earthquake_data['magnitude']}\n"
            f"- Location: {earthquake_data['location']}\n"
        )
        
        try:
            cache_key = f"{earthquake_data.get('detail_link', earthquake_data['date_time'])}-summary"
            cached = self._get_cache(cache_key)
            if cached:
                logger.info("✅ Using cached summary")
                return cached
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",  # Fixed model name
                config=types.GenerateContentConfig(system_instruction=self.system_instruction),
                contents=contents
            )
            
            summary = response.text
            self._set_cache(cache_key, summary)
            
            logger.info("✅ Generated new summary with Gemini")
            return summary
        
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}", exc_info=True)
            return self._fallback_summary(earthquake_data)
    
    def _parse_magnitude(self, magnitude_str):
        """Extract numeric magnitude"""
        import re
        match = re.search(r'\d+\.?\d*', magnitude_str)
        return float(match.group()) if match else 0.0
    
    def _fallback_summary(self, data):
        """Simple template if AI fails"""
        return (
            f"An earthquake with magnitude {data['magnitude']} occurred at {data['location']} "
            f"on {data['date_time']}. The depth was {data['depth']}. "
            f"Please stay alert and follow safety protocols. "
            f"Monitor official updates for more information."
        )
    
    def _get_cache(self, key):
        """Get from Redis cache"""
        try:
            if redis_client:
                value = redis_client.get(key)
                return value.decode('utf-8') if value else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def _set_cache(self, key, value, expiry=3600):
        """Set to Redis cache"""
        try:
            if redis_client:
                redis_client.setex(key, expiry, value)
        except Exception as e:
            logger.error(f"Cache set error: {e}")