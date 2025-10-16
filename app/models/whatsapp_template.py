from datetime import datetime
from sqlalchemy import UniqueConstraint
from app import db

class WhatsAppTemplate(db.Model):
    __tablename__ = 'whatsapp_templates'
    __table_args__ = {'extend_existing': True}
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    template_name = db.Column(db.String(255), nullable=False) # Removed unique=True from here
    status = db.Column(db.String(50), default='PENDING')
    category = db.Column(db.String(50), default='UTILITY')
    language = db.Column(db.String(20), nullable=False)
    body = db.Column(db.Text, nullable=True)
    components = db.Column(db.JSON, nullable=True)
    header_media_handle = db.Column(db.String(512), nullable=True)
    header_media_filename = db.Column(db.String(255), nullable=True)
    header_media_path = db.Column(db.String(512), nullable=True)
    wa_template_uid = db.Column(db.String(255), nullable=True) # Removed unique=True, as Meta's ID is globally unique by nature
    account_id = db.Column(db.Integer, db.ForeignKey('whatsapp_accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship('WhatsAppMessage', backref='template', lazy=True, foreign_keys='WhatsAppMessage.template_id')
    
    # Define a table-level compound unique constraint
    __table_args__ = (
        UniqueConstraint('template_name', 'account_id', name='uq_template_name_per_account'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'template_name': self.template_name,
            'status': self.status,
            'category': self.category,
            'language': self.language,
            'body': self.body,
            'components': self.components,
            'header_media_handle': self.header_media_handle,
            'header_media_filename': self.header_media_filename,
            'header_media_path': self.header_media_path,
            'wa_template_uid': self.wa_template_uid,
            'account_id': self.account_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }