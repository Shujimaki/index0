from bs4 import BeautifulSoup
from flask import jsonify
from urllib.parse import urljoin
import requests
from datetime import datetime

cached_data_latest = None
last_fetch_time_latest = None
CACHE_DURATION = 5 * 60
BASE_URL = 'https://earthquake.phivolcs.dost.gov.ph/'

def fetch_latest_earthquake_raw():
    """Fetch raw earthquake data without JSON wrapping"""
    global cached_data_latest, last_fetch_time_latest

    try:
        now = datetime.now()

        if cached_data_latest and last_fetch_time_latest and (now.second - last_fetch_time_latest.second) < CACHE_DURATION:
            return cached_data_latest
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': "keep-alive",
        }

        res = requests.get(BASE_URL, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        tables = soup.select('table.MsoNormalTable')

        for table in tables:
            try:
                row = table.select('tr')[1]
            except:
                continue

            cells = row.find_all('td')

            if not cells or len(cells) != 6:
                continue
        
            date_time_cell = cells[0]
            latitude_cell = cells[1]
            longitude_cell = cells[2]
            depth_cell = cells[3]
            magnitude_cell = cells[4]
            location_cell = cells[5]

            date_time = date_time_cell.find('a').get_text().strip()
            a_tag = date_time_cell.find('a')
            
            if a_tag and 'href' in a_tag.attrs:
                href = a_tag['href']
                normalized_path = href.replace('\\','/')
                detail_link = urljoin(BASE_URL, normalized_path)
            else:
                detail_link = None

            earthquake = {
                "date_time": date_time,
                "latitude": latitude_cell.get_text().strip(),
                "longitude": longitude_cell.get_text().strip(),
                "depth": depth_cell.get_text().strip(),
                "magnitude": magnitude_cell.get_text().strip(),
                "location": location_cell.get_text().strip(),
                "detail_link": detail_link
            }
        
        cached_data_latest = earthquake
        last_fetch_time_latest = now
        return earthquake
    
    except Exception as e:
        return None


def get_latest_earthquake():
    """API endpoint version with JSON response"""
    data = fetch_latest_earthquake_raw()
    
    if data:
        return jsonify({
            "success": True,
            "data": data,
            "cached": False
        })
    else:
        return jsonify({
            "success": False,
            "message": "Error fetching latest earthquake data"
        })