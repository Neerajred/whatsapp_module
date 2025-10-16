# # # # # app/services/whatsapp_api.py
# # # # import requests
# # # # import logging
# # # # from typing import Dict
# # # # # CORRECTED: Changed relative import '..' to absolute import from the project root
# # # # from config import Config
# # # # from ..models.whatsapp_account import WhatsAppAccount

# # # # logger = logging.getLogger(__name__)

# # # # class WhatsAppAPIError(Exception):
# # # #     """Custom exception for WhatsApp API errors"""
# # # #     def __init__(self, message, error_code=None, details=None):
# # # #         self.message = message
# # # #         self.error_code = error_code
# # # #         self.details = details
# # # #         super().__init__(self.message)

# # # # class WhatsAppAPIService:
# # # #     """
# # # #     Service class for all interactions with the Meta WhatsApp Business API.
# # # #     It requires a WhatsAppAccount object for initialization.
# # # #     """
    
# # # #     def __init__(self, account: WhatsAppAccount):
# # # #         if not account or not isinstance(account, WhatsAppAccount):
# # # #             raise ValueError("A valid WhatsAppAccount instance is required.")
        
# # # #         self.account = account
# # # #         self.base_url = f"{Config.META_API_BASE_URL}/{Config.META_API_VERSION}"
# # # #         self.headers = {
# # # #             'Authorization': f'Bearer {self.account.token}',
# # # #             'Content-Type': 'application/json'
# # # #         }

# # # #     def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
# # # #         """A centralized method to make API requests and handle errors."""
# # # #         url = f"{self.base_url}{endpoint}"
        
# # # #         try:
# # # #             response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, timeout=30)
            
# # # #             response_data = response.json()

# # # #             if response.status_code >= 400:
# # # #                 error = response_data.get('error', {})
# # # #                 error_message = error.get('message', 'An unknown API error occurred.')
# # # #                 error_code = error.get('code')
# # # #                 error_details = error.get('error_data')
# # # #                 logger.error(f"WhatsApp API Error {response.status_code}: {error_message} | Details: {error_details}")
# # # #                 raise WhatsAppAPIError(error_message, error_code, error_details)
            
# # # #             return response_data
            
# # # #         except requests.exceptions.RequestException as e:
# # # #             logger.error(f"Network error during WhatsApp API call: {e}")
# # # #             raise WhatsAppAPIError("Network error occurred while connecting to WhatsApp API.")

# # # #     def test_connection(self) -> Dict:
# # # #         """
# # # #         Tests the API credentials by making a simple GET request.
# # # #         This is used to validate if the account credentials are working.
# # # #         """
# # # #         # A simple, harmless endpoint to check authentication and permissions.
# # # #         endpoint = f"/{self.account.account_uid}/message_templates"
# # # #         params = {'limit': 1} # Limit to 1 for efficiency
        
# # # #         # This will raise WhatsAppAPIError on failure, which is caught in the controller.
# # # #         self._make_request('GET', endpoint, params=params)
        
# # # #         return {'success': True, 'message': 'Credentials are valid.'}

# # # #     def sync_templates(self) -> list:
# # # #         """
# # # #         Fetches all message templates associated with the business account from Meta.
# # # #         """
# # # #         endpoint = f"/{self.account.account_uid}/message_templates"
# # # #         params = {
# # # #             'fields': 'name,components,language,status,category,id',
# # # #             'limit': 100 # Fetch up to 100 templates
# # # #         }
        
# # # #         result = self._make_request('GET', endpoint, params=params)
# # # #         return result.get('data', [])

# # # #     def create_template(self, template_data: Dict) -> Dict:
# # # #         """
# # # #         Submits a new message template to Meta for approval.
# # # #         The payload must be correctly structured.
# # # #         """
# # # #         endpoint = f"/{self.account.account_uid}/message_templates"
# # # #         payload = {
# # # #             "name": template_data['template_name'],
# # # #             "language": template_data['language'],
# # # #             "category": template_data['category'].upper(),
# # # #             "components": template_data['components']
# # # #         }
# # # #         return self._make_request('POST', endpoint, data=payload)

# # # import requests
# # # import json
# # # import logging
# # # import os
# # # from typing import Dict, List, Optional, Any
# # # from werkzeug.datastructures import FileStorage

# # # # Correctly import from the root-level config file
# # # from config import config
# # # from app.models.whatsapp_account import WhatsAppAccount

# # # logger = logging.getLogger(__name__)


# # # class WhatsAppAPIError(Exception):
# # #     """Custom exception for WhatsApp API errors"""
# # #     def __init__(self, message, error_code=None, failure_type=None, meta_error=None):
# # #         self.message = message
# # #         self.error_code = error_code
# # #         self.failure_type = failure_type
# # #         self.meta_error = meta_error
# # #         super().__init__(self.message)

# # # class WhatsAppAPIService:
# # #     """Service class for interacting with Meta WhatsApp Business API"""
    
# # #     def __init__(self, account: WhatsAppAccount):
# # #         if not account:
# # #             raise ValueError("WhatsAppAPIService requires a valid account instance.")
# # #         self.account = account
# # #         self.base_url = f"{config['default'].META_API_BASE_URL}/{config['default'].META_API_VERSION}"
# # #         self.headers = {
# # #             'Authorization': f'Bearer {self.account.token}',
# # #             'Content-Type': 'application/json'
# # #         }

# # #     def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
# # #         """Make API request with error handling"""
# # #         url = f"{self.base_url}{endpoint}"
        
# # #         try:
# # #             response = requests.request(
# # #                 method=method,
# # #                 url=url,
# # #                 headers=self.headers,
# # #                 json=data,
# # #                 params=params,
# # #                 timeout=30
# # #             )
            
# # #             response_data = response.json()

# # #             if response.status_code >= 400:
# # #                 error_details = response_data.get('error', {})
# # #                 error_message = error_details.get('message', 'Unknown API error')
# # #                 error_code = error_details.get('code')
                
# # #                 logger.error(f"WhatsApp API error {response.status_code}: {error_message}")
# # #                 raise WhatsAppAPIError(error_message, error_code=error_code, meta_error=error_details)
            
# # #             return response_data
            
# # #         except requests.exceptions.RequestException as e:
# # #             logger.error(f"Network error during WhatsApp API call: {str(e)}")
# # #             raise WhatsAppAPIError(f"Network error: {str(e)}", failure_type='network')

# # #     def test_connection(self) -> Dict:
# # #         """Test connection to WhatsApp Business API"""
# # #         endpoint = f"/{self.account.phone_uid}"
# # #         return self._make_request('GET', endpoint, params={'fields': 'id'})
        
# # #     def sync_templates(self) -> List[Dict]:
# # #         """Sync templates from Meta API"""
# # #         endpoint = f"/{self.account.account_uid}/message_templates"
# # #         params = {
# # #             'fields': 'name,components,language,status,category,id',
# # #             'limit': 100
# # #         }
        
# # #         result = self._make_request('GET', endpoint, params=params)
# # #         return result.get('data', [])
    
# # #     def create_template(self, template_data: Dict) -> Dict:
# # #         """Create new message template"""
# # #         endpoint = f"/{self.account.account_uid}/message_templates"
# # #         return self._make_request('POST', endpoint, data=template_data)

# # #     def upload_media_resumable(self, file: FileStorage) -> str:
# # #         """
# # #         Uploads a media file to Meta's servers using the two-step resumable protocol.
# # #         """
# # #         file_name = file.filename
# # #         file_mimetype = file.mimetype
# # #         file_bytes = file.read()
# # #         file_length = len(file_bytes)

# # #         # --- Step 1: Start an upload session ---
# # #         start_session_url = f"{self.base_url}/{self.account.app_uid}/uploads"
# # #         params = {
# # #             'file_length': file_length,
# # #             'file_type': file_mimetype,
# # #             'file_name': file_name,
# # #             'access_token': self.account.token
# # #         }
        
# # #         try:
# # #             logger.info(f"Starting upload session for {file_name}")
# # #             session_response = requests.post(start_session_url, params=params, timeout=30)
# # #             session_data = session_response.json()

# # #             if session_response.status_code >= 400:
# # #                 error_details = session_data.get('error', {})
# # #                 raise WhatsAppAPIError(
# # #                     f"Failed to start upload session: {error_details.get('message', 'Unknown error')}",
# # #                     meta_error=error_details
# # #                 )

# # #             upload_session_id = session_data['id']
# # #             logger.info(f"Upload session started with ID: {upload_session_id}")

# # #             # --- Step 2: Upload the file binary data ---
# # #             # The upload URL uses a different base and the session ID from step 1
# # #             upload_url = f"https://graph.facebook.com/v23.0/{upload_session_id}"
# # #             upload_headers = {
# # #                 'Authorization': f'OAuth {self.account.token}',
# # #                 'file_offset': '0'
# # #             }

# # #             logger.info(f"Uploading file binary for session {upload_session_id}")
# # #             upload_response = requests.post(
# # #                 upload_url,
# # #                 headers=upload_headers,
# # #                 data=file_bytes,
# # #                 timeout=60 # Longer timeout for file upload
# # #             )
# # #             upload_data = upload_response.json()

# # #             if upload_response.status_code >= 400:
# # #                 error_details = upload_data.get('error', {})
# # #                 raise WhatsAppAPIError(
# # #                     f"Failed to upload file binary: {error_details.get('message', 'Unknown error')}",
# # #                     meta_error=error_details
# # #                 )
            
# # #             file_handle = upload_data['h']
# # #             logger.info(f"File uploaded successfully. Handle: {file_handle}")
            
# # #             return file_handle

# # #         except requests.exceptions.RequestException as e:
# # #             logger.error(f"Network error during media upload: {str(e)}")
# # #             raise WhatsAppAPIError(f"Network error during upload: {str(e)}", failure_type='network')

# # #     def send_template_message(self, to: str, template_name: str, language_code: str, components: List[Dict]) -> Dict:
# # #         """Send template message with dynamic components."""
# # #         endpoint = f"/{self.account.phone_uid}/messages"
        
# # #         data = {
# # #             "messaging_product": "whatsapp",
# # #             "to": to,
# # #             "type": "template",
# # #             "template": {
# # #                 "name": template_name,
# # #                 "language": {"code": language_code},
# # #                 "components": components
# # #             }
# # #         }
# # #         return self._make_request('POST', endpoint, data=data)

# # # File: app/services/whatsapp_api.py
# # import requests
# # import json
# # import logging
# # from typing import Dict, List, Optional
# # from werkzeug.datastructures import FileStorage

# # from config import config
# # from app.models.whatsapp_account import WhatsAppAccount

# # logger = logging.getLogger(__name__)

# # class WhatsAppAPIError(Exception):
# #     def __init__(self, message, error_code=None, failure_type=None, meta_error=None):
# #         self.message = message
# #         self.error_code = error_code
# #         self.failure_type = failure_type
# #         self.meta_error = meta_error
# #         super().__init__(self.message)

# # class WhatsAppAPIService:
# #     def __init__(self, account: WhatsAppAccount):
# #         if not account:
# #             raise ValueError("WhatsAppAPIService requires a valid account instance.")
# #         self.account = account
# #         self.base_url = f"{config['default'].META_API_BASE_URL}/{config['default'].META_API_VERSION}"
# #         self.headers = {'Authorization': f'Bearer {self.account.token}', 'Content-Type': 'application/json'}

# #     def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
# #         url = f"{self.base_url}{endpoint}"
# #         try:
# #             response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, timeout=30)
# #             response_data = response.json()
# #             if response.status_code >= 400:
# #                 error_details = response_data.get('error', {})
# #                 raise WhatsAppAPIError(error_details.get('message', 'Unknown API error'), error_code=error_details.get('code'), meta_error=error_details)
# #             return response_data
# #         except requests.exceptions.RequestException as e:
# #             raise WhatsAppAPIError(f"Network error: {str(e)}", failure_type='network')

# #     def test_connection(self) -> Dict:
# #         return self._make_request('GET', f"/{self.account.phone_uid}", params={'fields': 'id'})
        
# #     def sync_templates(self) -> List[Dict]:
# #         params = {'fields': 'name,components,language,status,category,id', 'limit': 100}
# #         result = self._make_request('GET', f"/{self.account.account_uid}/message_templates", params=params)
# #         return result.get('data', [])
    
# #     def create_template(self, template_data: Dict) -> Dict:
# #         return self._make_request('POST', f"/{self.account.account_uid}/message_templates", data=template_data)

# #     def upload_media_resumable(self, file: FileStorage) -> str:
# #         file_bytes = file.read()
# #         params = {
# #             'file_length': len(file_bytes), 'file_type': file.mimetype,
# #             'file_name': file.filename, 'access_token': self.account.token
# #         }
# #         try:
# #             session_response = requests.post(f"{self.base_url}/{self.account.app_uid}/uploads", params=params, timeout=30)
# #             session_data = session_response.json()
# #             if session_response.status_code >= 400:
# #                 raise WhatsAppAPIError(f"Failed to start upload session: {session_data.get('error', {}).get('message')}", meta_error=session_data.get('error'))
            
# #             upload_session_id = session_data['id']
# #             upload_headers = {'Authorization': f'OAuth {self.account.token}', 'file_offset': '0'}
# #             upload_response = requests.post(f"https://graph.facebook.com/v23.0/{upload_session_id}", headers=upload_headers, data=file_bytes, timeout=60)
# #             upload_data = upload_response.json()
# #             if upload_response.status_code >= 400:
# #                 raise WhatsAppAPIError(f"Failed to upload file binary: {upload_data.get('error', {}).get('message')}", meta_error=upload_data.get('error'))
            
# #             return upload_data['h']
# #         except requests.exceptions.RequestException as e:
# #             raise WhatsAppAPIError(f"Network error during upload: {str(e)}", failure_type='network')

# #     def send_template_message(self, to: str, template_name: str, language_code: str, components: List[Dict]) -> Dict:
# #         data = {
# #             "messaging_product": "whatsapp", "to": to, "type": "template",
# #             "template": {"name": template_name, "language": {"code": language_code}, "components": components}
# #         }
# #         return self._make_request('POST', f"/{self.account.phone_uid}/messages", data=data)


# # File: app/services/whatsapp_api.py
# import requests
# import json
# import logging
# from typing import Dict, List, Optional
# from werkzeug.datastructures import FileStorage

# from config import config
# from app.models.whatsapp_account import WhatsAppAccount

# logger = logging.getLogger(__name__)

# class WhatsAppAPIError(Exception):
#     def __init__(self, message, error_code=None, failure_type=None, meta_error=None):
#         self.message = message
#         self.error_code = error_code
#         self.failure_type = failure_type
#         self.meta_error = meta_error
#         super().__init__(self.message)

# class WhatsAppAPIService:
#     def __init__(self, account: WhatsAppAccount):
#         if not account:
#             raise ValueError("WhatsAppAPIService requires a valid account instance.")
#         self.account = account
#         self.base_url = f"{config['default'].META_API_BASE_URL}/{config['default'].META_API_VERSION}"
#         self.headers = {'Authorization': f'Bearer {self.account.token}', 'Content-Type': 'application/json'}

#     def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
#         url = f"{self.base_url}{endpoint}"
#         try:
#             response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, timeout=30)
#             response_data = response.json()
#             if response.status_code >= 400:
#                 error_details = response_data.get('error', {})
#                 raise WhatsAppAPIError(error_details.get('message', 'Unknown API error'), error_code=error_details.get('code'), meta_error=error_details)
#             return response_data
#         except requests.exceptions.RequestException as e:
#             raise WhatsAppAPIError(f"Network error: {str(e)}", failure_type='network')

#     def test_connection(self) -> Dict:
#         return self._make_request('GET', f"/{self.account.phone_uid}", params={'fields': 'id'})
        
#     def sync_templates(self) -> List[Dict]:
#         params = {'fields': 'name,components,language,status,category,id', 'limit': 100}
#         result = self._make_request('GET', f"/{self.account.account_uid}/message_templates", params=params)
#         return result.get('data', [])
    
#     def create_template(self, template_data: Dict) -> Dict:
#         return self._make_request('POST', f"/{self.account.account_uid}/message_templates", data=template_data)

#     def upload_media_resumable(self, file: FileStorage) -> str:
#         file_bytes = file.read()
#         params = { 'file_length': len(file_bytes), 'file_type': file.mimetype, 'access_token': self.account.token }
#         try:
#             session_response = requests.post(f"{self.base_url}/{self.account.app_uid}/uploads", params=params, timeout=30)
#             session_data = session_response.json()
#             if session_response.status_code >= 400:
#                 raise WhatsAppAPIError(f"Failed to start upload session: {session_data.get('error', {}).get('message')}", meta_error=session_data.get('error'))
            
#             upload_session_id = session_data['id']
#             upload_headers = {'Authorization': f'OAuth {self.account.token}', 'file_offset': '0'}
#             upload_response = requests.post(f"https://graph.facebook.com/{upload_session_id}", headers=upload_headers, data=file_bytes, timeout=60)
#             upload_data = upload_response.json()
#             if upload_response.status_code >= 400:
#                 raise WhatsAppAPIError(f"Failed to upload file binary: {upload_data.get('error', {}).get('message')}", meta_error=upload_data.get('error'))
            
#             return upload_data['h']
#         except requests.exceptions.RequestException as e:
#             raise WhatsAppAPIError(f"Network error during upload: {str(e)}", failure_type='network')

#     def upload_reusable_media(self, file: FileStorage) -> str:
#         url = f"{self.base_url}/{self.account.phone_uid}/media"
#         file.seek(0)
#         form_data = {'messaging_product': (None, 'whatsapp')}
#         files = {'file': (file.filename, file.read(), file.mimetype)}
#         upload_headers = {'Authorization': f'Bearer {self.account.token}'}
#         try:
#             response = requests.post(url, headers=upload_headers, data=form_data, files=files, timeout=60)
#             response_data = response.json()
#             if response.status_code >= 400:
#                 raise WhatsAppAPIError(f"Failed to upload reusable media: {response_data.get('error', {}).get('message')}", meta_error=response_data.get('error'))
#             media_id = response_data.get('id')
#             if not media_id:
#                 raise WhatsAppAPIError("Upload succeeded but did not return a media ID.")
#             return media_id
#         except requests.exceptions.RequestException as e:
#             raise WhatsAppAPIError(f"Network error during reusable media upload: {str(e)}", failure_type='network')

#     def send_template_message(self, to: str, template_name: str, language_code: str, components: List[Dict]) -> Dict:
#         data = {
#             "messaging_product": "whatsapp", "to": to, "type": "template",
#             "template": {"name": template_name, "language": {"code": language_code}, "components": components}
#         }
#         return self._make_request('POST', f"/{self.account.phone_uid}/messages", data=data)




# File: app/services/whatsapp_api.py
import requests
import json
import logging
from typing import Dict, List, Optional
from werkzeug.datastructures import FileStorage

from config import config
from app.models.whatsapp_account import WhatsAppAccount

logger = logging.getLogger(__name__)

class WhatsAppAPIError(Exception):
    def __init__(self, message, error_code=None, failure_type=None, meta_error=None):
        self.message = message
        self.error_code = error_code
        self.failure_type = failure_type
        self.meta_error = meta_error
        super().__init__(self.message)

class WhatsAppAPIService:
    def __init__(self, account: WhatsAppAccount):
        if not account:
            raise ValueError("WhatsAppAPIService requires a valid account instance.")
        self.account = account
        self.base_url = f"{config['default'].META_API_BASE_URL}/{config['default'].META_API_VERSION}"
        self.headers = {'Authorization': f'Bearer {self.account.token}', 'Content-Type': 'application/json'}

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, timeout=30)
            response_data = response.json()
            if response.status_code >= 400:
                error_details = response_data.get('error', {})
                raise WhatsAppAPIError(error_details.get('message', 'Unknown API error'), error_code=error_details.get('code'), meta_error=error_details)
            return response_data
        except requests.exceptions.RequestException as e:
            raise WhatsAppAPIError(f"Network error: {str(e)}", failure_type='network')

    def test_connection(self) -> Dict:
        return self._make_request('GET', f"/{self.account.phone_uid}", params={'fields': 'id'})
        
    def sync_templates(self) -> List[Dict]:
        params = {'fields': 'name,components,language,status,category,id', 'limit': 100}
        result = self._make_request('GET', f"/{self.account.account_uid}/message_templates", params=params)
        return result.get('data', [])
    
    def create_template(self, template_data: Dict) -> Dict:
        return self._make_request('POST', f"/{self.account.account_uid}/message_templates", data=template_data)

    def upload_media_resumable(self, file: FileStorage) -> str:
        file_bytes = file.read()
        params = { 'file_length': len(file_bytes), 'file_type': file.mimetype, 'access_token': self.account.token }
        try:
            session_response = requests.post(f"{self.base_url}/{self.account.app_uid}/uploads", params=params, timeout=30)
            session_data = session_response.json()
            if session_response.status_code >= 400:
                raise WhatsAppAPIError(f"Failed to start upload session: {session_data.get('error', {}).get('message')}", meta_error=session_data.get('error'))
            
            upload_session_id = session_data['id']
            upload_headers = {'Authorization': f'OAuth {self.account.token}', 'file_offset': '0'}
            upload_response = requests.post(f"https://graph.facebook.com/{upload_session_id}", headers=upload_headers, data=file_bytes, timeout=60)
            upload_data = upload_response.json()
            if upload_response.status_code >= 400:
                raise WhatsAppAPIError(f"Failed to upload file binary: {upload_data.get('error', {}).get('message')}", meta_error=upload_data.get('error'))
            
            return upload_data['h']
        except requests.exceptions.RequestException as e:
            raise WhatsAppAPIError(f"Network error during upload: {str(e)}", failure_type='network')

    def upload_reusable_media(self, file: FileStorage) -> str:
        url = f"{self.base_url}/{self.account.phone_uid}/media"
        file.seek(0)
        form_data = {'messaging_product': (None, 'whatsapp')}
        files = {'file': (file.filename, file.read(), file.mimetype)}
        upload_headers = {'Authorization': f'Bearer {self.account.token}'}
        try:
            response = requests.post(url, headers=upload_headers, data=form_data, files=files, timeout=60)
            response_data = response.json()
            if response.status_code >= 400:
                raise WhatsAppAPIError(f"Failed to upload reusable media: {response_data.get('error', {}).get('message')}", meta_error=response_data.get('error'))
            media_id = response_data.get('id')
            if not media_id:
                raise WhatsAppAPIError("Upload succeeded but did not return a media ID.")
            return media_id
        except requests.exceptions.RequestException as e:
            raise WhatsAppAPIError(f"Network error during reusable media upload: {str(e)}", failure_type='network')

    def send_template_message(self, to: str, template_name: str, language_code: str, components: List[Dict]) -> Dict:
        data = {
            "messaging_product": "whatsapp", "to": to, "type": "template",
            "template": {"name": template_name, "language": {"code": language_code}, "components": components}
        }
        return self._make_request('POST', f"/{self.account.phone_uid}/messages", data=data)
    
    def upload_media_from_file(self, file_path: str) -> str:
        """Upload media from a local file path and return the media ID"""
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
                form_data = {'messaging_product': 'whatsapp'}
                url = f"{self.base_url}/{self.account.phone_uid}/media"
                
                upload_headers = {'Authorization': f'Bearer {self.account.token}'}
                
                response = requests.post(
                    url, 
                    headers=upload_headers, 
                    data=form_data, 
                    files=files, 
                    timeout=60
                )
                
                response_data = response.json()
                if response.status_code >= 400:
                    raise WhatsAppAPIError(
                        f"Failed to upload media: {response_data.get('error', {}).get('message')}", 
                        meta_error=response_data.get('error')
                    )
                
                media_id = response_data.get('id')
                if not media_id:
                    raise WhatsAppAPIError("Upload succeeded but did not return a media ID.")
                
                return media_id
                
        except FileNotFoundError:
            raise WhatsAppAPIError(f"Media file not found: {file_path}")
        except requests.exceptions.RequestException as e:
            raise WhatsAppAPIError(f"Network error during media upload: {str(e)}", failure_type='network')

    def refresh_media_id(self, file_path: str) -> str:
        """Refresh media ID for a template (wrapper around upload_media_from_file)"""
        return self.upload_media_from_file(file_path)
    
    def delete_template(self, template_uid: str) -> Dict:
        """Delete a message template from Meta"""
        if not template_uid:
            raise WhatsAppAPIError("Template UID is required for deletion.")
        
        endpoint = f"/{self.account.account_uid}/message_templates"
        params = {'name': template_uid}  # Meta API uses name parameter for deletion
        
        return self._make_request('DELETE', endpoint, params=params)