from app import database
from datetime import datetime

class User(database.Model):
    __tablename__ = 'users'
    
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), unique=True, nullable=False, index=True)
    email = database.Column(database.String(150), unique=True, nullable=False, index=True)
    created_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'