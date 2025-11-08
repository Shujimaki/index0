"""Philippine provinces and cities with coordinates"""

PHILIPPINE_LOCATIONS = {
    'Metro Manila': {
        'Manila': (14.5995, 120.9842),
        'Quezon City': (14.6760, 121.0437),
        'Makati': (14.5547, 121.0244),
        'Pasig': (14.5764, 121.0851),
        'Taguig': (14.5176, 121.0509),
        'Mandaluyong': (14.5794, 121.0359),
        'Pasay': (14.5378, 121.0014),
        'Caloocan': (14.6488, 120.9830),
        'Marikina': (14.6507, 121.1029),
        'Valenzuela': (14.6937, 120.9830),
    },
    'Cebu': {
        'Cebu City': (10.3157, 123.8854),
        'Mandaue': (10.3237, 123.9227),
        'Lapu-Lapu': (10.3103, 123.9494),
        'Talisay': (10.2449, 123.8494),
    },
    'Davao': {
        'Davao City': (7.1907, 125.4553),
        'Tagum': (7.4479, 125.8078),
        'Panabo': (7.3072, 125.6839),
    },
    'Bulacan': {
        'Malolos': (14.8433, 120.8114),
        'Meycauayan': (14.7342, 120.9528),
        'San Jose del Monte': (14.8139, 121.0453),
    },
    'Cavite': {
        'Imus': (14.4297, 120.9367),
        'Bacoor': (14.4587, 120.9536),
        'Dasmariñas': (14.3294, 120.9367),
        'Cavite City': (14.4791, 120.8964),
    },
    'Laguna': {
        'Santa Cruz': (14.2819, 121.4161),
        'Calamba': (14.2120, 121.1655),
        'Biñan': (14.3386, 121.0800),
        'San Pedro': (14.3553, 121.0178),
    },
    'Rizal': {
        'Antipolo': (14.5864, 121.1754),
        'Cainta': (14.5778, 121.1222),
        'Taytay': (14.5574, 121.1328),
    },
    'Pampanga': {
        'San Fernando': (15.0280, 120.6864),
        'Angeles': (15.1450, 120.5887),
        'Mabalacat': (15.2250, 120.5717),
    },
    'Pangasinan': {
        'Lingayen': (16.0183, 120.2297),
        'Dagupan': (16.0433, 120.3336),
        'Urdaneta': (15.9761, 120.5711),
    },
    'Iloilo': {
        'Iloilo City': (10.7202, 122.5621),
        'Passi': (11.1083, 122.6333),
    },
    'Negros Occidental': {
        'Bacolod': (10.6767, 122.9500),
        'Silay': (10.7969, 122.9728),
    },
    'Negros Oriental': {
        'Dumaguete': (9.3068, 123.3054),
        'Bais': (9.5908, 123.1219),
    },
    'Leyte': {
        'Tacloban': (11.2447, 125.0039),
        'Ormoc': (11.0064, 124.6075),
    },
    'Albay': {
        'Legazpi': (13.1391, 123.7436),
        'Tabaco': (13.3594, 123.7333),
    },
    'Batangas': {
        'Batangas City': (13.7565, 121.0583),
        'Lipa': (13.9411, 121.1622),
    },
}

def get_all_provinces():
    """Get list of all provinces"""
    return sorted(PHILIPPINE_LOCATIONS.keys())

def get_cities_in_province(province):
    """Get list of cities in a province"""
    return sorted(PHILIPPINE_LOCATIONS.get(province, {}).keys())

def get_coordinates(province, city):
    """Get coordinates for a city"""
    if province in PHILIPPINE_LOCATIONS:
        if city in PHILIPPINE_LOCATIONS[province]:
            return PHILIPPINE_LOCATIONS[province][city]
    return None