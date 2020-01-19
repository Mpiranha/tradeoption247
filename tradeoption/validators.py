from django.core.exceptions import ValidationError

def check_positive(value):
    if not value >= 0:
        raise ValidationError("Sorry, Balance shold be positive")