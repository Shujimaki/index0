from app import database
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(database.Model):
    __tablename__ = 'users'
    
    id = database.Column(database.Integer, primary_key=True)
    full_name = database.Column(database.String(150), nullable=False)
    email_address = database.Column(database.String(150), unique=True, nullable=False, index=True)
    password_hash = database.Column(database.String(256), nullable=False)
    user_province = database.Column(database.String(100), nullable=False)
    user_city = database.Column(database.String(100), nullable=False)
    registered_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
    is_active = database.Column(database.Boolean, default=True)
    
    notification_settings = database.relationship('NotificationSettings', backref='owner', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.full_name,
            'email': self.email_address,
            'province': self.user_province,
            'city': self.user_city,
            'registered': self.registered_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.id}: {self.full_name}>'

class NotificationSettings(database.Model):
    __tablename__ = 'notification_settings'
    
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False, unique=True)
    
    magnitude_threshold = database.Column(database.Float, default=3.0, nullable=False)
    monitor_location_type = database.Column(database.String(20), default='near_me', nullable=False)
    alternate_province = database.Column(database.String(100))
    alternate_city = database.Column(database.String(100))
    add_safety_tips = database.Column(database.Boolean, default=True, nullable=False)
    proximity_range_km = database.Column(database.Float, default=100.0, nullable=False)
    
    settings_created = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
    settings_modified = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'min_magnitude': self.magnitude_threshold,
            'location_type': self.monitor_location_type,
            'custom_province': self.alternate_province,
            'custom_city': self.alternate_city,
            'include_tips': self.add_safety_tips,
            'range_km': self.proximity_range_km
        }

class SeismicEvent(database.Model):
    __tablename__ = 'seismic_events'
    
    id = database.Column(database.Integer, primary_key=True)
    event_identifier = database.Column(database.String(200), unique=True, nullable=False, index=True)
    event_magnitude = database.Column(database.Float, nullable=False)
    event_location = database.Column(database.String(300), nullable=False)
    latitude_coord = database.Column(database.Float)
    longitude_coord = database.Column(database.Float)
    depth_km = database.Column(database.Float)
    occurred_at = database.Column(database.DateTime, nullable=False)
    has_been_processed = database.Column(database.Boolean, default=False, nullable=False)
    recorded_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'event_id': self.event_identifier,
            'magnitude': self.event_magnitude,
            'location': self.event_location,
            'coordinates': {'lat': self.latitude_coord, 'lon': self.longitude_coord},
            'depth': self.depth_km,
            'time': self.occurred_at.isoformat()
        }