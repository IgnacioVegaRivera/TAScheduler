from django import template

register = template.Library()

@register.filter
def format_phone(value):
    # format a 10-digit phone number (example: 1234567890 -> 123-456-7890)
    if isinstance(value, str) and len(value) == 10 and value.isdigit():
        return f"{value[:3]}-{value[3:6]}-{value[6:]}"
    return value