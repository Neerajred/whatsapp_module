# import re
# from typing import Optional, Tuple, List, Dict

# def validate_template_name(name: str) -> Tuple[bool, Optional[str]]:
#     """Validate WhatsApp template name according to Meta's rules."""
#     if not name or len(name) > 512:
#         return False, "Template name must be between 1 and 512 characters."
    
#     if not re.match(r'^[a-z0-9_]+$', name):
#         return False, "Template name can only contain lowercase letters, numbers, and underscores."
    
#     return True, None

# def validate_template_payload(data: dict) -> Tuple[bool, Optional[List[str]]]:
#     """
#     Validates the entire template payload structure before submission.
#     """
#     errors = []
    
#     # --- Top-Level Field Validation ---
#     required_fields = ['name', 'language', 'category', 'account_id', 'components']
#     for field in required_fields:
#         if field not in data:
#             errors.append(f"Missing required top-level field: '{field}'.")
    
#     if errors:
#         return False, errors # Stop validation if basic fields are missing

#     # --- Field Content Validation ---
#     if not isinstance(data['name'], str) or not validate_template_name(data['name'])[0]:
#         errors.append("Field 'name' is invalid. Use lowercase letters, numbers, and underscores.")
    
#     if not isinstance(data['language'], str) or len(data['language']) < 2:
#         errors.append("Field 'language' must be a valid language code (e.g., 'en_US').")
        
#     valid_categories = ['MARKETING', 'UTILITY', 'AUTHENTICATION']
#     if data.get('category').upper() not in valid_categories:
#         errors.append(f"Field 'category' must be one of: {', '.join(valid_categories)}.")

#     if not isinstance(data['account_id'], int):
#         errors.append("Field 'account_id' must be an integer.")

#     # --- Components Validation ---
#     if not isinstance(data['components'], list) or not data['components']:
#         errors.append("Field 'components' must be a non-empty list.")
#     else:
#         has_body = any(comp.get('type') == 'BODY' for comp in data['components'])
#         if not has_body:
#             errors.append("The 'components' list must contain at least one 'BODY' component.")

#     return len(errors) == 0, errors if errors else None

# File: app/utils/validators.py
import re
import phonenumbers
from typing import Optional, Tuple, List, Dict

def validate_phone_number(phone: str, country_code: str = None) -> Tuple[bool, Optional[str]]:
    """
    Validate phone number format and convert to E.164.
    """
    try:
        if not phone:
            return False, "Phone number is required"
        
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone, country_code)
        
        if not phonenumbers.is_valid_number(parsed_number):
            return False, "Invalid phone number format."
        
        # Format to E.164 standard (e.g., +14155552671)
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return True, formatted_number
        
    except phonenumbers.NumberParseException as e:
        return False, f"Unable to parse phone number: {e}"

def validate_template_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate WhatsApp template name according to Meta's rules."""
    if not name or len(name) > 512:
        return False, "Template name must be between 1 and 512 characters."
    
    if not re.match(r'^[a-z0-9_]+$', name):
        return False, "Template name can only contain lowercase letters, numbers, and underscores."
    
    return True, None

def validate_template_payload(data: dict) -> Tuple[bool, Optional[List[str]]]:
    """
    Validates the entire template payload structure before submission.
    """
    errors = []
    
    # --- Top-Level Field Validation ---
    required_fields = ['name', 'language', 'category', 'account_id', 'components']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required top-level field: '{field}'.")
    
    if errors:
        return False, errors # Stop validation if basic fields are missing

    # --- Field Content Validation ---
    if not isinstance(data['name'], str) or not validate_template_name(data['name'])[0]:
        errors.append("Field 'name' is invalid. Use lowercase letters, numbers, and underscores.")
    
    if not isinstance(data['language'], str) or len(data['language']) < 2:
        errors.append("Field 'language' must be a valid language code (e.g., 'en_US').")
        
    valid_categories = ['MARKETING', 'UTILITY', 'AUTHENTICATION']
    if data.get('category').upper() not in valid_categories:
        errors.append(f"Field 'category' must be one of: {', '.join(valid_categories)}.")

    if not isinstance(data['account_id'], int):
        errors.append("Field 'account_id' must be an integer.")

    # --- Components Validation ---
    if not isinstance(data['components'], list) or not data['components']:
        errors.append("Field 'components' must be a non-empty list.")
    else:
        has_body = any(comp.get('type') == 'BODY' for comp in data['components'])
        if not has_body:
            errors.append("The 'components' list must contain at least one 'BODY' component.")

    return len(errors) == 0, errors if errors else None