# File: app/models/whatsapp_message.py
from datetime import datetime
from app import db

class WhatsAppMessage(db.Model):
    __tablename__ = 'whatsapp_messages'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('whatsapp_accounts.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('whatsapp_templates.id'), nullable=True)  # Fixed foreign key
    recipient_phone = db.Column(db.String(20), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'inbound' or 'outbound'
    status = db.Column(db.String(20), default='sent')  # 'sent', 'delivered', 'read', 'failed'
    meta_message_id = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'template_id': self.template_id,
            'recipient_phone': self.recipient_phone,
            'direction': self.direction,
            'status': self.status,
            'meta_message_id': self.meta_message_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }