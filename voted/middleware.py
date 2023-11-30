from datetime import timedelta

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from product.models import User


class UserIDMiddleware(MiddlewareMixin):
    """
    Check if the session has a user id attribute. Create a new user if necessary.
    """

    def process_request(self, request):
        if not request.session.get("user_id"):
            # create user
            user = User.objects.create()
            # add user id to session data
            request.session["user_id"] = str(user.id)


EXTENSION_THRESHOLD = 7
EXTENSION_AMOUNT = 7


class ExtendSessionMiddleware(MiddlewareMixin):
    """
    Extend a user's session after it reaches the threshold.
    """

    def process_request(self, request):
        now = timezone.now()
        if request.session.get_expiry_date() < now + timedelta(days=EXTENSION_THRESHOLD):
            request.session.set_expiry(now + timedelta(days=EXTENSION_AMOUNT))
