# File: app/models/whatsapp_account.py
from datetime import datetime
from app import db

class WhatsAppAccount(db.Model):
    __tablename__ = 'whatsapp_accounts'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    app_uid = db.Column(db.String(255), nullable=False)
    app_secret = db.Column(db.String(255), nullable=False)
    account_uid = db.Column(db.String(255), nullable=False)
    phone_uid = db.Column(db.String(255), nullable=False)
    token = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - fixed with proper foreign key references
    templates = db.relationship('WhatsAppTemplate', backref='account', lazy=True, foreign_keys='WhatsAppTemplate.account_id')
    messages = db.relationship('WhatsAppMessage', backref='account', lazy=True, foreign_keys='WhatsAppMessage.account_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'app_uid': self.app_uid,
            'app_secret': self.app_secret,
            'account_uid': self.account_uid,
            'phone_uid': self.phone_uid,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }