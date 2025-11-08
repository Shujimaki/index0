from geopy.distance import geodesic
from app.ph_locations import get_coordinates
import logging

logger = logging.getLogger(__name__)

class LocationAnalyzer:
    """Analyze earthquake locations and affected areas"""
    
    @staticmethod
    def parse_magnitude(magnitude_text):
        """Parse magnitude from text"""
        import re
        pattern = re.search(r'\d+\.?\d*', magnitude_text)
        return float(pattern.group()) if pattern else 0.0
    
    @staticmethod
    def parse_coordinates(lat_text, lon_text):
        """Convert coordinate strings to floats"""
        try:
            lat_val = float(lat_text.replace('°', '').strip())
            lon_val = float(lon_text.replace('°', '').strip())
            return lat_val, lon_val
        except:
            return None, None
    
    @staticmethod
    def calculate_affected_radius(magnitude):
        """Calculate impact radius based on magnitude"""
        base_km = 30
        return base_km + (magnitude * 25)
    
    @staticmethod
    def calculate_distance(coord1, coord2):
        """Calculate distance between two points in km"""
        return geodesic(coord1, coord2).kilometers
    
    @staticmethod
    def is_location_affected(province, city, quake_coords, radius_km):
        """Check if a location is within affected radius"""
        city_coords = get_coordinates(province, city)
        
        if not city_coords or not quake_coords or not quake_coords[0] or not quake_coords[1]:
            return False
        
        distance = LocationAnalyzer.calculate_distance(city_coords, quake_coords)
        return distance <= radius_km