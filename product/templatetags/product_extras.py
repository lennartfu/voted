from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def time_status(timestamp):
    if timestamp < now():
        return "Beendet"
    diff = timestamp - now()
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    message = "🔴 Endet in "
    if days > 0:
        if days == 1:
            message += "einem Tag"
        else:
            message += f"{days} Tagen"
    elif hours > 0:
        if hours == 1:
            message += "einer Stunde"
        else:
            message += f"{hours} Stunden"
    elif minutes > 0:
        if minutes == 1:
            message += "einer Minute"
        else:
            message += f"{minutes} Minuten"
    else:
        message = "Beendet"
    return message
