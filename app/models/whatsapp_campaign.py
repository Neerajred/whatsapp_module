# [file name]: models/whatsapp_campaign.py
from datetime import datetime
from .. import db

class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='DRAFT')
    
    # Relationships
    account_id = db.Column(db.Integer, db.ForeignKey('whatsapp_accounts.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('whatsapp_templates.id'), nullable=False)
    
    # Campaign details
    recipient_list = db.Column(db.Text)  # JSON or CSV data
    start_time = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'account_id': self.account_id,
            'template_id': self.template_id,
            'recipient_list': self.recipient_list,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CampaignRecipient(db.Model):
    __tablename__ = 'campaign_recipients'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('marketing_campaigns.id'), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='PENDING')
    
    # Meta API data
    meta_message_id = db.Column(db.String(255))
    
    # Timestamps
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    
    # Error handling
    error_message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'phone_number': self.phone_number,
            'status': self.status,
            'meta_message_id': self.meta_message_id,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'error_message': self.error_message
        }