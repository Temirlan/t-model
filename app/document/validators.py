""" Validators """
import os
from django.core.exceptions import ValidationError

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 10485760


def validate_file_extension(value):
  """ Check file extensions: pdf, docx, html """
  ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
  # valid_extensions = ['.pdf', '.docx', '.html']
  valid_extensions = ['.pdf']

  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Unsupported file type')
  else:
    limit = MAX_UPLOAD_SIZE
    if value.size > limit:
      raise ValidationError(
          'File is too large. File size must not exceed 10 MiB.')
    else:
      pass
