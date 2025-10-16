# # # File: app/controllers/api.py
# # from flask import Blueprint, request, jsonify
# # from flask_jwt_extended import create_access_token, jwt_required
# # from werkzeug.utils import secure_filename
# # import os
# # import json

# # from app import db
# # from app.models.whatsapp_account import WhatsAppAccount
# # from app.models.whatsapp_template import WhatsAppTemplate
# # from app.models.whatsapp_message import WhatsAppMessage
# # from app.services.whatsapp_api import WhatsAppAPIService, WhatsAppAPIError
# # from app.utils.validators import validate_template_name, validate_template_payload, validate_phone_number

# # api_bp = Blueprint('api', __name__, url_prefix='/api/whatsapp')

# # @api_bp.route('/auth/generate_token', methods=['GET'])
# # def generate_token():
# #     access_token = create_access_token(identity={'username': 'dev_user'})
# #     return jsonify(access_token=access_token)

# # @api_bp.route('/accounts', methods=['GET'])
# # @jwt_required()
# # def get_accounts():
# #     accounts = WhatsAppAccount.query.all()
# #     return jsonify({'success': True, 'data': [account.to_dict() for account in accounts]})

# # @api_bp.route('/accounts', methods=['POST'])
# # @jwt_required()
# # def create_account():
# #     data = request.get_json()
# #     required_fields = ['name', 'app_uid', 'app_secret', 'account_uid', 'phone_uid', 'token']
# #     if not all(field in data for field in required_fields):
# #         return jsonify({'error': 'Missing one or more required fields.'}), 400
    
# #     new_account = WhatsAppAccount(**data)
# #     db.session.add(new_account)
# #     db.session.commit()
# #     return jsonify({'success': True, 'message': 'Account created successfully.', 'data': new_account.to_dict()}), 201

# # @api_bp.route('/accounts/<int:account_id>/test', methods=['POST'])
# # @jwt_required()
# # def test_account_credentials(account_id):
# #     account = db.session.get(WhatsAppAccount, account_id)
# #     if not account:
# #         return jsonify({'error': 'Account not found'}), 404
        
# #     try:
# #         service = WhatsAppAPIService(account)
# #         service.test_connection()
# #         account.status = 'VALIDATED'
# #         db.session.commit()
# #         return jsonify({'success': True, 'message': 'Account credentials are valid.'})
# #     except WhatsAppAPIError as e:
# #         account.status = 'ERROR'
# #         db.session.commit()
# #         return jsonify({'error': 'Failed to validate account credentials.', 'details': e.message, 'meta_error': e.meta_error}), 400

# # @api_bp.route('/accounts/<int:account_id>/sync_templates', methods=['POST'])
# # @jwt_required()
# # def sync_templates(account_id):
# #     account = db.session.get(WhatsAppAccount, account_id)
# #     if not account:
# #         return jsonify({'error': 'Account not found'}), 404

# #     try:
# #         service = WhatsAppAPIService(account)
# #         meta_templates = service.sync_templates()
# #         created_count, updated_count = 0, 0
        
# #         for t_data in meta_templates:
# #             existing_template = WhatsAppTemplate.query.filter_by(wa_template_uid=t_data['id']).first()
# #             body_text = next((comp.get('text', '') for comp in t_data.get('components', []) if comp.get('type') == 'BODY'), None)

# #             if existing_template:
# #                 existing_template.name = t_data['name']
# #                 existing_template.status = t_data['status']
# #                 existing_template.category = t_data['category']
# #                 existing_template.language = t_data['language']
# #                 existing_template.components = t_data.get('components', [])
# #                 existing_template.body = body_text
# #                 updated_count += 1
# #             else:
# #                 new_template = WhatsAppTemplate(
# #                     name=t_data['name'], template_name=t_data['name'], status=t_data['status'],
# #                     category=t_data['category'], language=t_data['language'], wa_template_uid=t_data['id'],
# #                     account_id=account_id, components=t_data.get('components', []), body=body_text)
# #                 db.session.add(new_template)
# #                 created_count += 1
        
# #         db.session.commit()
# #         return jsonify({'success': True, 'message': 'Templates synced successfully.',
# #                         'summary': {'total_fetched': len(meta_templates), 'created': created_count, 'updated': updated_count}})
# #     except WhatsAppAPIError as e:
# #         return jsonify({'error': 'Failed to sync templates due to an API error.', 'details': e.message}), 400

# # @api_bp.route('/templates/create_with_media', methods=['POST'])
# # @jwt_required()
# # def create_template_with_media():
# #     if 'template_data' not in request.form or 'file' not in request.files:
# #         return jsonify({'error': "Request must include 'template_data' and 'file' parts."}), 400

# #     try:
# #         template_data = json.loads(request.form['template_data'])
# #     except json.JSONDecodeError:
# #         return jsonify({'error': "'template_data' must be a valid JSON string."}), 400

# #     file = request.files['file']
# #     if file.filename == '' or not allowed_file(file.filename):
# #         return jsonify({'error': 'A valid file must be provided.'}), 400

# #     is_valid, errors = validate_template_payload(template_data)
# #     if not is_valid:
# #         return jsonify({'error': 'Invalid template data.', 'details': errors}), 400

# #     account = db.session.get(WhatsAppAccount, template_data.get('account_id'))
# #     if not account or account.status != 'VALIDATED':
# #         return jsonify({'error': 'A valid, validated account is required.'}), 400

# #     try:
# #         service = WhatsAppAPIService(account)
# #         file.seek(0)
# #         temp_file_handle = service.upload_media_resumable(file)
# #         file.seek(0)
# #         permanent_media_id = service.upload_reusable_media(file)
        
# #         header_component = next((comp for comp in template_data['components'] if comp['type'] == 'HEADER'), None)
# #         if not header_component:
# #             return jsonify({'error': "Template data must include a 'HEADER' component for media."}), 400
        
# #         header_component['example'] = {'header_handle': [temp_file_handle]}

# #         meta_payload = {
# #             'name': template_data['name'], 'language': template_data['language'],
# #             'category': template_data['category'], 'components': template_data['components'],
# #             'allow_category_change': True
# #         }
# #         meta_response = service.create_template(meta_payload)

# #         new_template = WhatsAppTemplate(
# #             name=template_data['name'], template_name=template_data['name'],
# #             language=template_data['language'], category=template_data['category'],
# #             components=template_data['components'], account_id=template_data['account_id'],
# #             wa_template_uid=meta_response.get('id'), status='PENDING',
# #             header_media_handle=permanent_media_id
# #         )
# #         db.session.add(new_template)
# #         db.session.commit()
        
# #         return jsonify({
# #             'success': True, 'message': 'Template with media submitted and permanent handle saved.', 
# #             'data': new_template.to_dict()
# #         }), 201
        
# #     except WhatsAppAPIError as e:
# #         return jsonify({'error': 'Failed to process template with media.', 'details': e.message, 'meta_error': e.meta_error}), 400
# #     except Exception as e:
# #         db.session.rollback()
# #         return jsonify({'error': 'An unexpected internal server error occurred.', 'details': str(e)}), 500

# # @api_bp.route('/messages/send_template', methods=['POST'])
# # @jwt_required()
# # def send_template_message():
# #     data = request.get_json()
# #     required_fields = ['account_id', 'template_name', 'recipient_phone_number']
# #     if not all(field in data for field in required_fields):
# #         return jsonify({'error': 'Missing required fields: account_id, template_name, recipient_phone_number.'}), 400

# #     account = db.session.get(WhatsAppAccount, data['account_id'])
# #     if not account or account.status != 'VALIDATED':
# #         return jsonify({'error': 'A valid, validated account is required.'}), 400

# #     template = WhatsAppTemplate.query.filter_by(
# #         template_name=data['template_name'],
# #         account_id=data['account_id']
# #     ).first()

# #     if not template or template.status != 'APPROVED':
# #         return jsonify({'error': 'A valid, approved template is required.'}), 400
    
# #     is_valid_phone, phone_e164 = validate_phone_number(data['recipient_phone_number'])
# #     if not is_valid_phone:
# #         return jsonify({'error': 'Invalid recipient phone number.'}), 400
    
# #     final_components = []
    
# #     if template.header_media_handle:
# #         header_component = {"type": "header", "parameters": [{
# #             "type": "image",
# #             "image": {"id": template.header_media_handle}
# #         }]}
# #         final_components.append(header_component)
        
# #     if 'body_params' in data and data['body_params']:
# #         body_component = {"type": "body", "parameters": []}
# #         for text_param in data['body_params']:
# #             body_component['parameters'].append({"type": "text", "text": str(text_param)})
# #         final_components.append(body_component)
    
# #     try:
# #         service = WhatsAppAPIService(account)
# #         meta_response = service.send_template_message(
# #             to=phone_e164,
# #             template_name=template.template_name,
# #             language_code=template.language,
# #             components=final_components
# #         )

# #         message_id = meta_response.get('messages', [{}])[0].get('id')
# #         new_message = WhatsAppMessage(
# #             account_id=account.id, template_id=template.id, recipient_phone=phone_e164,
# #             direction='outbound', status='sent', meta_message_id=message_id, content=json.dumps(data)
# #         )
# #         db.session.add(new_message)
# #         db.session.commit()

# #         return jsonify({'success': True, 'message': 'Template message sent successfully.', 'meta_response': meta_response})
# #     except WhatsAppAPIError as e:
# #         return jsonify({'error': 'Failed to send message.', 'details': e.message, 'meta_error': e.meta_error}), 400
# #     except Exception as e:
# #         db.session.rollback()
# #         return jsonify({'error': 'An unexpected internal server error occurred while sending.', 'details': str(e)}), 500

# # # --- Helper Functions ---
# # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'mp4'}
# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# # File: app/controllers/api.py
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token, jwt_required
# from werkzeug.utils import secure_filename
# import os
# import json

# from app import db
# from app.models.whatsapp_account import WhatsAppAccount
# from app.models.whatsapp_template import WhatsAppTemplate
# from app.models.whatsapp_message import WhatsAppMessage
# from app.services.whatsapp_api import WhatsAppAPIService, WhatsAppAPIError
# from app.utils.validators import validate_template_name, validate_template_payload, validate_phone_number

# api_bp = Blueprint('api', __name__, url_prefix='/api/whatsapp')

# @api_bp.route('/auth/generate_token', methods=['GET'])
# def generate_token():
#     access_token = create_access_token(identity={'username': 'dev_user'})
#     return jsonify(access_token=access_token)

# @api_bp.route('/accounts', methods=['GET'])
# @jwt_required()
# def get_accounts():
#     accounts = WhatsAppAccount.query.all()
#     return jsonify({'success': True, 'data': [account.to_dict() for account in accounts]})

# @api_bp.route('/accounts', methods=['POST'])
# @jwt_required()
# def create_account():
#     data = request.get_json()
#     required_fields = ['name', 'app_uid', 'app_secret', 'account_uid', 'phone_uid', 'token']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing one or more required fields.'}), 400
    
#     new_account = WhatsAppAccount(**data)
#     db.session.add(new_account)
#     db.session.commit()
#     return jsonify({'success': True, 'message': 'Account created successfully.', 'data': new_account.to_dict()}), 201

# @api_bp.route('/accounts/<int:account_id>/test', methods=['POST'])
# @jwt_required()
# def test_account_credentials(account_id):
#     account = db.session.get(WhatsAppAccount, account_id)
#     if not account:
#         return jsonify({'error': 'Account not found'}), 404
        
#     try:
#         service = WhatsAppAPIService(account)
#         service.test_connection()
#         account.status = 'VALIDATED'
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'Account credentials are valid.'})
#     except WhatsAppAPIError as e:
#         account.status = 'ERROR'
#         db.session.commit()
#         return jsonify({'error': 'Failed to validate account credentials.', 'details': e.message, 'meta_error': e.meta_error}), 400

# @api_bp.route('/accounts/<int:account_id>/sync_templates', methods=['POST'])
# @jwt_required()
# def sync_templates(account_id):
#     account = db.session.get(WhatsAppAccount, account_id)
#     if not account:
#         return jsonify({'error': 'Account not found'}), 404

#     try:
#         service = WhatsAppAPIService(account)
#         meta_templates = service.sync_templates()
#         created_count, updated_count = 0, 0
        
#         for t_data in meta_templates:
#             existing_template = WhatsAppTemplate.query.filter_by(wa_template_uid=t_data['id']).first()
#             body_text = next((comp.get('text', '') for comp in t_data.get('components', []) if comp.get('type') == 'BODY'), None)

#             if existing_template:
#                 existing_template.name = t_data['name']
#                 existing_template.status = t_data['status']
#                 existing_template.category = t_data['category']
#                 existing_template.language = t_data['language']
#                 existing_template.components = t_data.get('components', [])
#                 existing_template.body = body_text
#                 updated_count += 1
#             else:
#                 new_template = WhatsAppTemplate(
#                     name=t_data['name'], template_name=t_data['name'], status=t_data['status'],
#                     category=t_data['category'], language=t_data['language'], wa_template_uid=t_data['id'],
#                     account_id=account_id, components=t_data.get('components', []), body=body_text)
#                 db.session.add(new_template)
#                 created_count += 1
        
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'Templates synced successfully.',
#                         'summary': {'total_fetched': len(meta_templates), 'created': created_count, 'updated': updated_count}})
#     except WhatsAppAPIError as e:
#         return jsonify({'error': 'Failed to sync templates due to an API error.', 'details': e.message}), 400

# @api_bp.route('/templates/create_with_media', methods=['POST'])
# @jwt_required()
# def create_template_with_media():
#     if 'template_data' not in request.form or 'file' not in request.files:
#         return jsonify({'error': "Request must include 'template_data' and 'file' parts."}), 400

#     try:
#         template_data = json.loads(request.form['template_data'])
#     except json.JSONDecodeError:
#         return jsonify({'error': "'template_data' must be a valid JSON string."}), 400

#     file = request.files['file']
#     if file.filename == '' or not allowed_file(file.filename):
#         return jsonify({'error': 'A valid file must be provided.'}), 400

#     is_valid, errors = validate_template_payload(template_data)
#     if not is_valid:
#         return jsonify({'error': 'Invalid template data.', 'details': errors}), 400

#     account = db.session.get(WhatsAppAccount, template_data.get('account_id'))
#     if not account or account.status != 'VALIDATED':
#         return jsonify({'error': 'A valid, validated account is required.'}), 400

#     try:
#         service = WhatsAppAPIService(account)
#         file.seek(0)
#         temp_file_handle = service.upload_media_resumable(file)
#         file.seek(0)
#         permanent_media_id = service.upload_reusable_media(file)
        
#         header_component = next((comp for comp in template_data['components'] if comp['type'] == 'HEADER'), None)
#         if not header_component:
#             return jsonify({'error': "Template data must include a 'HEADER' component for media."}), 400
        
#         header_component['example'] = {'header_handle': [temp_file_handle]}

#         meta_payload = {
#             'name': template_data['name'], 'language': template_data['language'],
#             'category': template_data['category'], 'components': template_data['components'],
#             'allow_category_change': True
#         }
#         meta_response = service.create_template(meta_payload)

#         new_template = WhatsAppTemplate(
#             name=template_data['name'], template_name=template_data['name'],
#             language=template_data['language'], category=template_data['category'],
#             components=template_data['components'], account_id=template_data['account_id'],
#             wa_template_uid=meta_response.get('id'), status='PENDING',
#             header_media_handle=permanent_media_id
#         )
#         db.session.add(new_template)
#         db.session.commit()
        
#         return jsonify({
#             'success': True, 'message': 'Template with media submitted and permanent handle saved.', 
#             'data': new_template.to_dict()
#         }), 201
        
#     except WhatsAppAPIError as e:
#         return jsonify({'error': 'Failed to process template with media.', 'details': e.message, 'meta_error': e.meta_error}), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An unexpected internal server error occurred.', 'details': str(e)}), 500

# @api_bp.route('/messages/send_template', methods=['POST'])
# @jwt_required()
# def send_template_message():
#     data = request.get_json()
#     required_fields = ['account_id', 'template_name', 'recipient_phone_number']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Missing required fields: account_id, template_name, recipient_phone_number.'}), 400

#     account = db.session.get(WhatsAppAccount, data['account_id'])
#     if not account or account.status != 'VALIDATED':
#         return jsonify({'error': 'A valid, validated account is required.'}), 400

#     template = WhatsAppTemplate.query.filter_by(
#         template_name=data['template_name'],
#         account_id=data['account_id']
#     ).first()

#     if not template or template.status != 'APPROVED':
#         return jsonify({'error': 'A valid, approved template is required.'}), 400
    
#     is_valid_phone, phone_e164 = validate_phone_number(data['recipient_phone_number'])
#     if not is_valid_phone:
#         return jsonify({'error': 'Invalid recipient phone number.'}), 400
    
#     final_components = []
    
#     # Automatically use the saved permanent media ID for the header
#     if template.header_media_handle:
#         header_component = {"type": "header", "parameters": [{
#             "type": "image",
#             "image": {"id": template.header_media_handle}
#         }]}
#         final_components.append(header_component)
        
#     # Build body component from parameters
#     if 'body_params' in data and data['body_params']:
#         body_component = {"type": "body", "parameters": []}
#         for text_param in data['body_params']:
#             body_component['parameters'].append({"type": "text", "text": str(text_param)})
#         final_components.append(body_component)
    
#     try:
#         service = WhatsAppAPIService(account)
#         meta_response = service.send_template_message(
#             to=phone_e164,
#             template_name=template.template_name,
#             language_code=template.language,
#             components=final_components
#         )

#         message_id = meta_response.get('messages', [{}])[0].get('id')
#         new_message = WhatsAppMessage(
#             account_id=account.id, template_id=template.id, recipient_phone=phone_e164,
#             direction='outbound', status='sent', meta_message_id=message_id, content=json.dumps(data)
#         )
#         db.session.add(new_message)
#         db.session.commit()

#         return jsonify({'success': True, 'message': 'Template message sent successfully.', 'meta_response': meta_response})
#     except WhatsAppAPIError as e:
#         return jsonify({'error': 'Failed to send message.', 'details': e.message, 'meta_error': e.meta_error}), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An unexpected internal server error occurred while sending.', 'details': str(e)}), 500

# # --- Helper Functions ---
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'mp4'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# File: app/controllers/api.py
import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.utils import secure_filename
import os
import json

from app import db
from app.models.whatsapp_account import WhatsAppAccount
from app.models.whatsapp_template import WhatsAppTemplate
from app.models.whatsapp_message import WhatsAppMessage
from app.services.whatsapp_api import WhatsAppAPIService, WhatsAppAPIError
from app.utils.validators import validate_template_name, validate_template_payload, validate_phone_number
from app.services.media_storage import MediaStorageService

api_bp = Blueprint('api', __name__, url_prefix='/api/whatsapp')
media_storage = MediaStorageService()

@api_bp.route('/auth/generate_token', methods=['GET'])
def generate_token():
    access_token = create_access_token(identity={'username': 'dev_user'})
    return jsonify(access_token=access_token)

@api_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    accounts = WhatsAppAccount.query.all()
    return jsonify({'success': True, 'data': [account.to_dict() for account in accounts]})

@api_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    data = request.get_json()
    required_fields = ['name', 'app_uid', 'app_secret', 'account_uid', 'phone_uid', 'token']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing one or more required fields.'}), 400
    
    new_account = WhatsAppAccount(**data)
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Account created successfully.', 'data': new_account.to_dict()}), 201

@api_bp.route('/accounts/<int:account_id>/test', methods=['POST'])
@jwt_required()
def test_account_credentials(account_id):
    account = db.session.get(WhatsAppAccount, account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
        
    try:
        service = WhatsAppAPIService(account)
        service.test_connection()
        account.status = 'VALIDATED'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Account credentials are valid.'})
    except WhatsAppAPIError as e:
        account.status = 'ERROR'
        db.session.commit()
        return jsonify({'error': 'Failed to validate account credentials.', 'details': e.message, 'meta_error': e.meta_error}), 400

@api_bp.route('/accounts/<int:account_id>/sync_templates', methods=['POST'])
@jwt_required()
def sync_templates(account_id):
    account = db.session.get(WhatsAppAccount, account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    try:
        service = WhatsAppAPIService(account)
        meta_templates = service.sync_templates()
        created_count, updated_count = 0, 0
        
        for t_data in meta_templates:
            existing_template = WhatsAppTemplate.query.filter_by(wa_template_uid=t_data['id']).first()
            body_text = next((comp.get('text', '') for comp in t_data.get('components', []) if comp.get('type') == 'BODY'), None)

            if existing_template:
                existing_template.name = t_data['name']
                existing_template.status = t_data['status']
                existing_template.category = t_data['category']
                existing_template.language = t_data['language']
                existing_template.components = t_data.get('components', [])
                existing_template.body = body_text
                updated_count += 1
            else:
                new_template = WhatsAppTemplate(
                    name=t_data['name'], template_name=t_data['name'], status=t_data['status'],
                    category=t_data['category'], language=t_data['language'], wa_template_uid=t_data['id'],
                    account_id=account_id, components=t_data.get('components', []), body=body_text)
                db.session.add(new_template)
                created_count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Templates synced successfully.',
                        'summary': {'total_fetched': len(meta_templates), 'created': created_count, 'updated': updated_count}})
    except WhatsAppAPIError as e:
        return jsonify({'error': 'Failed to sync templates due to an API error.', 'details': e.message}), 400

@api_bp.route('/templates/create_with_media', methods=['POST'])
@jwt_required()
def create_template_with_media():
    if 'template_data' not in request.form or 'file' not in request.files:
        return jsonify({'error': "Request must include 'template_data' and 'file' parts."}), 400

    try:
        template_data = json.loads(request.form['template_data'])
    except json.JSONDecodeError:
        return jsonify({'error': "'template_data' must be a valid JSON string."}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'A valid file must be provided.'}), 400

    is_valid, errors = validate_template_payload(template_data)
    if not is_valid:
        return jsonify({'error': 'Invalid template data.', 'details': errors}), 400

    account = db.session.get(WhatsAppAccount, template_data.get('account_id'))
    if not account or account.status != 'VALIDATED':
        return jsonify({'error': 'A valid, validated account is required.'}), 400

    try:
        service = WhatsAppAPIService(account)
        
        # Save file locally first
        saved_file_info = media_storage.save_file(file, file.filename)
        
        # Upload to WhatsApp to get media ID for template creation
        file.seek(0)
        temp_file_handle = service.upload_media_resumable(file)
        file.seek(0)
        permanent_media_id = service.upload_reusable_media(file)
        
        header_component = next((comp for comp in template_data['components'] if comp['type'] == 'HEADER'), None)
        if not header_component:
            return jsonify({'error': "Template data must include a 'HEADER' component for media."}), 400
        
        header_component['example'] = {'header_handle': [temp_file_handle]}

        meta_payload = {
            'name': template_data['name'], 'language': template_data['language'],
            'category': template_data['category'], 'components': template_data['components'],
            'allow_category_change': True
        }
        
        print("Meta Payload:", json.dumps(meta_payload, indent=2))  # Debugging line
        meta_response = service.create_template(meta_payload)

        new_template = WhatsAppTemplate(
            name=template_data['name'], template_name=template_data['name'],
            language=template_data['language'], category=template_data['category'],
            components=template_data['components'], account_id=template_data['account_id'],
            wa_template_uid=meta_response.get('id'), status='PENDING',
            header_media_handle=permanent_media_id,
            header_media_filename=saved_file_info['filename'],
            header_media_path=saved_file_info['file_path']
        )
        db.session.add(new_template)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Template with media submitted and files saved locally.', 
            'data': new_template.to_dict(),
            'file_info': saved_file_info
        }), 201
        
    except WhatsAppAPIError as e:
        return jsonify({'error': 'Failed to process template with media.', 'details': e.message, 'meta_error': e.meta_error}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected internal server error occurred.', 'details': str(e)}), 500
    

@api_bp.route('/messages/send_template', methods=['POST'])
@jwt_required()
def send_template_message():
    data = request.get_json()
    required_fields = ['account_id', 'template_name', 'recipient_phone_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: account_id, template_name, recipient_phone_number.'}), 400

    account = db.session.get(WhatsAppAccount, data['account_id'])
    if not account or account.status != 'VALIDATED':
        return jsonify({'error': 'A valid, validated account is required.'}), 400

    template = WhatsAppTemplate.query.filter_by(
        template_name=data['template_name'],
        account_id=data['account_id']
    ).first()

    if not template or template.status != 'APPROVED':
        return jsonify({'error': 'A valid, approved template is required.'}), 400
    
    is_valid_phone, phone_e164 = validate_phone_number(data['recipient_phone_number'])
    if not is_valid_phone:
        return jsonify({'error': 'Invalid recipient phone number.'}), 400
    
    final_components = []
    current_media_id = None
    
    # Handle header media (if template has media)
    if template.header_media_handle and template.header_media_path:
        try:
            service = WhatsAppAPIService(account)
            
            # First, try with the existing media ID
            current_media_id = template.header_media_handle
            header_component = {
                "type": "header", 
                "parameters": [{
                    "type": "image",
                    "image": {"id": current_media_id}
                }]
            }
            final_components.append(header_component)
            
        except Exception as e:
            logger.warning(f"Error preparing media component: {str(e)}")
    
    # Build body component from parameters
    if 'body_params' in data and data['body_params']:
        body_component = {"type": "body", "parameters": []}
        for text_param in data['body_params']:
            body_component['parameters'].append({"type": "text", "text": str(text_param)})
        final_components.append(body_component)
    
    try:
        service = WhatsAppAPIService(account)
        
        # Attempt to send the message
        max_retries = 2
        for attempt in range(max_retries):
            try:
                meta_response = service.send_template_message(
                    to=phone_e164,
                    template_name=template.template_name,
                    language_code=template.language,
                    components=final_components
                )
                break  # Success, break out of retry loop
                
            except WhatsAppAPIError as e:
                if attempt < max_retries - 1 and "not a valid whatsapp business account media attachment ID" in e.message:
                    # Media ID is invalid, try to refresh it
                    logger.info(f"Media ID invalid, attempting refresh (attempt {attempt + 1})")
                    
                    if template.header_media_path and media_storage.file_exists(template.header_media_filename):
                        try:
                            # Refresh the media ID
                            new_media_id = service.refresh_media_id(template.header_media_path)
                            
                            # Update the template with new media ID
                            template.header_media_handle = new_media_id
                            db.session.commit()
                            
                            # Update the components with new media ID
                            final_components = [comp for comp in final_components if comp.get('type') != 'header']
                            header_component = {
                                "type": "header", 
                                "parameters": [{
                                    "type": "image",
                                    "image": {"id": new_media_id}
                                }]
                            }
                            final_components.append(header_component)
                            
                            logger.info(f"Media ID refreshed successfully: {new_media_id}")
                            continue  # Retry with new media ID
                            
                        except Exception as refresh_error:
                            logger.error(f"Failed to refresh media ID: {str(refresh_error)}")
                            # Fall back to sending without media
                            final_components = [comp for comp in final_components if comp.get('type') != 'header']
                            continue
                    else:
                        # No local file available, send without media
                        final_components = [comp for comp in final_components if comp.get('type') != 'header']
                        continue
                else:
                    # Other error or final attempt failed
                    raise
        
        message_id = meta_response.get('messages', [{}])[0].get('id')
        new_message = WhatsAppMessage(
            account_id=account.id, template_id=template.id, recipient_phone=phone_e164,
            direction='outbound', status='sent', meta_message_id=message_id, content=json.dumps(data)
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            'success': True, 
            'message': 'Template message sent successfully.', 
            'meta_response': meta_response,
            'media_refreshed': current_media_id != template.header_media_handle
        })
        
    except WhatsAppAPIError as e:
        error_info = {
            'error': 'Failed to send message.',
            'details': e.message,
            'meta_error': e.meta_error,
            'debug_info': {
                'template_name': template.template_name,
                'media_id_used': template.header_media_handle,
                'has_local_file': template.header_media_path and media_storage.file_exists(template.header_media_filename)
            }
        }
        return jsonify(error_info), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected internal server error occurred while sending.', 'details': str(e)}), 500
    
@api_bp.route('/templates/create', methods=['POST'])
@jwt_required()
def create_template():
    """
    Create or preview a flexible WhatsApp template (Text-Only or with Text Header).
    Handles body, footer, and all button types correctly.
    Add '?preview=true' to the URL to get the payload without calling the Meta API.
    """
    data = request.get_json()
    
    # --- 1. Validation ---
    required_fields = ['name', 'language', 'category', 'body', 'account_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    is_valid_name, name_error = validate_template_name(data['name'])
    if not is_valid_name:
        return jsonify({'error': f'Invalid template name: {name_error}'}), 400
    
    account = db.session.get(WhatsAppAccount, data['account_id'])
    if not account or account.status != 'VALIDATED':
        return jsonify({'error': 'A valid, validated account is required.'}), 400
    
    try:
        # --- 2. Dynamic Component Construction ---
        components = []
        
        # Add TEXT HEADER component if provided
        if 'header' in data and data['header'] and data['header'].get('format') == 'TEXT':
            header_data = data['header']
            component = {"type": "HEADER", "format": "TEXT"}
            component['text'] = header_data.get('text', '')
            if 'example' in header_data and header_data['example'].get('header_text'):
                component['example'] = {"header_text": header_data['example']['header_text']}
            components.append(component)

        # Add BODY component
        body_component = {"type": "BODY", "text": data['body']}
        if data.get('example_body'):
            body_component["example"] = {"body_text": [data['example_body']]}
        components.append(body_component)
        
        # Add FOOTER component
        if data.get('footer'):
            components.append({"type": "FOOTER", "text": data['footer']})
            
        # Add BUTTONS component
        if 'buttons' in data and data['buttons']:
            components.append({
                "type": "BUTTONS",
                "buttons": data['buttons']
            })
            
        # --- 3. Prepare Final Payload ---
        meta_payload = {
            'name': data['name'],
            'language': data['language'],
            'category': data['category'].upper(),
            'components': components,
            'allow_category_change': True
        }
        
        # --- 4. Preview Logic ---
        if request.args.get('preview', 'false').lower() == 'true':
            return jsonify({
                'success': True,
                'message': 'Payload preview generated successfully.',
                'payload_preview': meta_payload
            }), 200

        # --- 5. API Call and Database Save ---
        print("--- Attempting to send the following payload to Meta API ---")
        print(json.dumps(meta_payload, indent=4))
        
        service = WhatsAppAPIService(account)
        meta_response = service.create_template(meta_payload)
        
        new_template = WhatsAppTemplate(
            name=data['name'],
            template_name=data['name'],
            language=data['language'],
            category=data['category'],
            components=components,
            account_id=data['account_id'],
            wa_template_uid=meta_response.get('id'),
            status='PENDING'
        )
        db.session.add(new_template)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Template created successfully.',
            'data': new_template.to_dict(),
            'meta_response': meta_response
        }), 201
        
    except WhatsAppAPIError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create template via Meta API.', 'details': e.message, 'meta_error': e.meta_error}), 400
    except Exception as e:
        db.session.rollback()
        print(traceback.format_exc()) 
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500
    
@api_bp.route('/templates/<int:template_id>/refresh_media', methods=['POST'])
@jwt_required()
def refresh_template_media(template_id):
    """Refresh the media ID for a template if it has expired"""
    template = db.session.get(WhatsAppTemplate, template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    account = db.session.get(WhatsAppAccount, template.account_id)
    if not account or account.status != 'VALIDATED':
        return jsonify({'error': 'A valid, validated account is required.'}), 400
    
    # Check if we have the original file or need to re-upload
    # For now, we'll assume we need to get a new media ID
    # In a real implementation, you'd want to store the original file
    
    return jsonify({'error': 'Media refresh not implemented. Media IDs expire after 30 days.'}), 501


# File: app/controllers/api.py (add these new endpoints)

@api_bp.route('/templates/<int:template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    """Delete a WhatsApp template"""
    template = db.session.get(WhatsAppTemplate, template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    try:
        # Optional: Also delete from Meta API (commented out for safety)
        # account = db.session.get(WhatsAppAccount, template.account_id)
        # if account and account.status == 'VALIDATED':
        #     service = WhatsAppAPIService(account)
        #     service.delete_template(template.wa_template_uid)
        
        # Delete local media file if exists
        if template.header_media_path and media_storage.file_exists(template.header_media_filename):
            media_storage.delete_file(template.header_media_filename)
        
        db.session.delete(template)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Template deleted successfully.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete template.', 'details': str(e)}), 500

# @api_bp.route('/templates/create_text', methods=['POST'])
# @jwt_required()
# def create_text_template():
#     """Create a text-only WhatsApp template (no media)"""
#     data = request.get_json()
    
#     # Validate required fields
#     required_fields = ['name', 'language', 'category', 'body', 'account_id']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
#     # Validate template name
#     is_valid_name, name_error = validate_template_name(data['name'])
#     if not is_valid_name:
#         return jsonify({'error': f'Invalid template name: {name_error}'}), 400
    
#     account = db.session.get(WhatsAppAccount, data['account_id'])
#     if not account or account.status != 'VALIDATED':
#         return jsonify({'error': 'A valid, validated account is required.'}), 400
    
#     try:
#         service = WhatsAppAPIService(account)
        
#         # Prepare components for Meta API
#         components = []
        
#         # Add body component
#         if data['body']:
#             components.append({
#                 "type": "BODY",
#                 "text": data['body'],
#                 "example": {
#                     "body_text": [data.get('example_body', [])] if data.get('example_body') else []
#                 }
#             })
        
#         # Add footer if provided
#         if data.get('footer'):
#             components.append({
#                 "type": "FOOTER",
#                 "text": data['footer']
#             })
        
#         # Add buttons if provided
#         buttons = data.get('buttons', [])
#         for button in buttons:
#             if button.get('type') == 'QUICK_REPLY':
#                 components.append({
#                     "type": "BUTTONS",
#                     "buttons": [{
#                         "type": "QUICK_REPLY",
#                         "text": button.get('text', '')
#                     }]
#                 })
        
#         # Prepare payload for Meta API
#         meta_payload = {
#             'name': data['name'],
#             'language': data['language'],
#             'category': data['category'].upper(),
#             'components': components
#         }
        
#         # Create template in Meta
#         meta_response = service.create_template(meta_payload)
        
#         # Save to database
#         new_template = WhatsAppTemplate(
#             name=data['name'],
#             template_name=data['name'],
#             language=data['language'],
#             category=data['category'],
#             body=data['body'],
#             components=components,
#             account_id=data['account_id'],
#             wa_template_uid=meta_response.get('id'),
#             status='PENDING'
#         )
        
#         db.session.add(new_template)
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': 'Text template created successfully.',
#             'data': new_template.to_dict(),
#             'meta_response': meta_response
#         }), 201
        
#     except WhatsAppAPIError as e:
#         db.session.rollback()
#         return jsonify({
#             'error': 'Failed to create template via Meta API.',
#             'details': e.message,
#             'meta_error': e.meta_error
#         }), 400
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500


# @api_bp.route('/templates/create_text', methods=['POST'])
# @jwt_required()
# def create_template():
#     """
#     Create or preview a flexible WhatsApp template.
#     Handles headers (TEXT/MEDIA), body, footer, and all button types correctly.
#     Add '?preview=true' to the URL to get the payload without calling the Meta API.
#     """
#     data = request.get_json()
    
#     # --- 1. Validation ---
#     required_fields = ['name', 'language', 'category', 'body', 'account_id']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
#     is_valid_name, name_error = validate_template_name(data['name'])
#     if not is_valid_name:
#         return jsonify({'error': f'Invalid template name: {name_error}'}), 400
    
#     account = db.session.get(WhatsAppAccount, data['account_id'])
#     if not account or account.status != 'VALIDATED':
#         return jsonify({'error': 'A valid, validated account is required.'}), 400
    
#     try:
#         # --- 2. Dynamic Component Construction ---
#         components = []
        
#         # Add HEADER component if provided in the request
#         if 'header' in data and data['header']:
#             header_data = data['header']
#             header_format = header_data.get('format', 'TEXT').upper()
#             component = {"type": "HEADER", "format": header_format}

#             if header_format == 'TEXT':
#                 component['text'] = header_data.get('text', '')
#                 if 'example' in header_data and header_data['example'].get('header_text'):
#                     component['example'] = {"header_text": header_data['example']['header_text']}
#             else: # For MEDIA types (IMAGE, VIDEO, DOCUMENT)
#                 if 'example' in header_data:
#                     if header_data['example'].get('header_handle'):
#                         component['example'] = {"header_handle": header_data['example']['header_handle']}
#                     elif header_data['example'].get('header_url'):
#                         component['example'] = {"header_url": header_data['example']['header_url']}
#             components.append(component)

#         # Add BODY component (required by Meta)
#         body_component = {"type": "BODY", "text": data['body']}
#         if data.get('example_body'):
#             body_component["example"] = {"body_text": [data['example_body']]}
#         components.append(body_component)
        
#         # Add FOOTER component if provided
#         if data.get('footer'):
#             components.append({"type": "FOOTER", "text": data['footer']})
            
#         # Add a single BUTTONS component if any buttons are provided
#         if 'buttons' in data and data['buttons']:
#             components.append({
#                 "type": "BUTTONS",
#                 "buttons": data['buttons']  # Pass the entire list of button objects
#             })
            
#         # --- 3. Prepare Final Payload ---
#         meta_payload = {
#             'name': data['name'],
#             'language': data['language'],
#             'category': data['category'].upper(),
#             'components': components,
#             'allow_category_change': True
#         }
        
#         # --- 4. Preview Logic ---
#         if request.args.get('preview', 'false').lower() == 'true':
#             return jsonify({
#                 'success': True,
#                 'message': 'Payload preview generated successfully.',
#                 'payload_preview': meta_payload
#             }), 200

#         # --- 5. API Call and Database Save ---
#         print("--- Attempting to send the following payload to Meta API ---")
#         print(json.dumps(meta_payload, indent=4))
        
#         service = WhatsAppAPIService(account)
#         meta_response = service.create_template(meta_payload)
        
#         new_template = WhatsAppTemplate(
#             name=data['name'],
#             template_name=data['name'],
#             language=data['language'],
#             category=data['category'],
#             components=components,
#             account_id=data['account_id'],
#             wa_template_uid=meta_response.get('id'),
#             status='PENDING'
#         )
#         db.session.add(new_template)
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': 'Template created successfully.',
#             'data': new_template.to_dict(),
#             'meta_response': meta_response
#         }), 201
        
#     except WhatsAppAPIError as e:
#         db.session.rollback()
#         return jsonify({
#             'error': 'Failed to create template via Meta API.',
#             'details': e.message, 'meta_error': e.meta_error
#         }), 400
#     except Exception as e:
#         db.session.rollback()
#         print(traceback.format_exc()) 
#         return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500


@api_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_templates():
    """Get all templates with optional filtering"""
    account_id = request.args.get('account_id')
    status = request.args.get('status')
    
    query = WhatsAppTemplate.query
    
    if account_id:
        query = query.filter_by(account_id=account_id)
    
    if status:
        query = query.filter_by(status=status)
    
    templates = query.order_by(WhatsAppTemplate.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [template.to_dict() for template in templates],
        'count': len(templates)
    })


