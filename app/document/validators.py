import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.docx', '.html']
    
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file type')
    else:
        limit = 5242880
        if value.size > limit:
            raise ValidationError('File is too large. File size must not exceed 5 MiB.')
