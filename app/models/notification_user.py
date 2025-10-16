# [file name]: models/notification_user.py
from datetime import datetime
from .. import db

class NotificationUser(db.Model):
    __tablename__ = 'notification_users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('whatsapp_accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'account_id': self.account_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }