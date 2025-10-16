# File: app/services/media_storage.py
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

class MediaStorageService:
    """Service for handling local media file storage"""
    
    def __init__(self, base_upload_folder=None):
        self.base_upload_folder = base_upload_folder or current_app.config.get('MEDIA_UPLOAD_FOLDER', 'media_uploads')
        
        # Create base directory if it doesn't exist
        if not os.path.exists(self.base_upload_folder):
            os.makedirs(self.base_upload_folder)
    
    def generate_unique_filename(self, original_filename):
        """Generate a unique filename to avoid conflicts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        safe_filename = secure_filename(original_filename)
        name, ext = os.path.splitext(safe_filename)
        return f"{name}_{timestamp}_{unique_id}{ext}"
    
    def save_file(self, file_stream, filename, subfolder='templates'):
        """Save file to local storage and return the path"""
        # Generate unique filename
        unique_filename = self.generate_unique_filename(filename)
        
        # Create subfolder path
        subfolder_path = os.path.join(self.base_upload_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        
        # Full file path
        file_path = os.path.join(subfolder_path, unique_filename)
        
        # Save the file
        file_stream.seek(0)
        file_stream.save(file_path)
        
        return {
            'filename': unique_filename,
            'original_filename': filename,
            'file_path': file_path,
            'relative_path': os.path.join(subfolder, unique_filename)
        }
    
    def get_file_path(self, filename, subfolder='templates'):
        """Get the full path of a stored file"""
        return os.path.join(self.base_upload_folder, subfolder, filename)
    
    def file_exists(self, filename, subfolder='templates'):
        """Check if a file exists"""
        file_path = self.get_file_path(filename, subfolder)
        return os.path.exists(file_path)
    
    def delete_file(self, filename, subfolder='templates'):
        """Delete a stored file"""
        file_path = self.get_file_path(filename, subfolder)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False