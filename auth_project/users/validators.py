from django.core.exceptions import ValidationError
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError('The password must contain at least one uppercase letter.')
        if not re.findall('[a-z]', password):
            raise ValidationError('The password must contain at least one lowercase letter.')
        if not re.findall('[0-9]', password):
            raise ValidationError('The password must contain at least one digit.')
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError('The password must contain at least one special character.')
    
    def get_help_text(self):
        return "Your password must contain uppercase, lowercase, digit, and special character."