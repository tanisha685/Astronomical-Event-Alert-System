# app.py
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
import geocoder
from timezonefinder import TimezoneFinder
import pytz
import ics
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG = {
    "location": {
        "auto_detect": True,
        "manual_lat": 40.7128,
        "manual_lng": -74.0060
    },
    "search_radius_km": 500
}

class EventFetcher:
    def __init__(self):
        self.location = self._get_location()
        self.timezone = self._get_timezone()
        
    def _get_location(self):
        """Get current location (auto or manual)"""
        if CONFIG["location"]["auto_detect"]:
            g = geocoder.ip('me')
            if g.ok:
                return g.latlng
            print("Could not auto-detect location, using manual coordinates")
        return [CONFIG["location"]["manual_lat"], CONFIG["location"]["manual_lng"]]
    
    def _get_timezone(self):
        """Get timezone for current location"""
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=self.location[0], lng=self.location[1])
        return pytz.timezone(timezone_str)
    
    def fetch_events(self):
        """Fetch all astronomical events"""
        events = []
        events.extend(self._fetch_nasa_events())
        events.extend(self._fetch_meteor_showers())
        return self._filter_visible_events(events)
    
    def _fetch_nasa_events(self):
        """Get close approach data from NASA API"""
        url = "https://ssd-api.jpl.nasa.gov/cad.api"
        params = {
            'dist-max': '0.2',
            'date-min': datetime.now().strftime('%Y-%m-%d'),
            'date-max': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            events = []
            
            for item in data.get('data', []):
                event = {
                    'id': f"nasa-{item[0]}-{item[3]}",
                    'name': f"{item[0]} Close Approach",
                    'description': f"{item[0]} will be {item[4]} AU from Earth on {item[3]}",
                    'start': datetime.strptime(item[3], '%Y-%b-%d %H:%M').isoformat(),
                    'end': None,
                    'type': 'planetary',
                    'source': 'NASA',
                    'visible': True
                }
                events.append(event)
            return events
        except Exception as e:
            print(f"Error fetching NASA data: {e}")
            return []
    
    def _fetch_meteor_showers(self):
        """Get meteor shower data from a public API"""
        url = "https://meteor-shower-api.herokuapp.com/meteorshowers"
        
        try:
            response = requests.get(url)
            data = response.json()
            events = []
            
            for shower in data:
                peak_date = datetime.strptime(shower['peak'], '%Y-%m-%d')
                if peak_date > datetime.now():
                    event = {
                        'id': f"meteor-{shower['name']}-{shower['peak']}",
                        'name': f"{shower['name']} Meteor Shower",
                        'description': f"Peak activity on {shower['peak']}. {shower['description']}",
                        'start': peak_date.isoformat(),
                        'end': (peak_date + timedelta(days=1)).isoformat(),
                        'type': 'meteor',
                        'source': 'Meteor Shower API',
                        'visible': True
                    }
                    events.append(event)
            return events
        except Exception as e:
            print(f"Error fetching meteor shower data: {e}")
            return []
    
    def _filter_visible_events(self, events):
        """Filter events to those visible in the user's location"""
        filtered = []
        for event in events:
            local_time = datetime.fromisoformat(event['start']).astimezone(self.timezone)
            hour = local_time.hour
            if 18 <= hour <= 23 or 0 <= hour <= 6:
                event['local_time'] = local_time.strftime('%Y-%m-%d %H:%M')
                filtered.append(event)
        return filtered

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events')
def get_events():
    fetcher = EventFetcher()
    events = fetcher.fetch_events()
    return jsonify(events)

@app.route('/api/calendar')
def download_calendar():
    fetcher = EventFetcher()
    events = fetcher.fetch_events()
    
    calendar = ics.Calendar()
    for event in events:
        ics_event = ics.Event(
            name=event['name'],
            begin=datetime.fromisoformat(event['start']),
            end=datetime.fromisoformat(event['end']) if event['end'] else datetime.fromisoformat(event['start']) + timedelta(hours=1),
            description=event['description']
        )
        calendar.events.add(ics_event)
    
    return calendar.serialize(), 200, {
        'Content-Type': 'text/calendar',
        'Content-Disposition': 'attachment; filename=astronomy_events.ics'
    }

if __name__ == '__main__':
    app.run(debug=True)