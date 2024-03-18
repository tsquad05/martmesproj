from django.utils import timezone
from django.http import HttpResponseForbidden

def password_reset_cooldown_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        cooldown_period = timezone.timedelta(minutes=1)  # Adjust cooldown period as needed
        user = request.user
        if user.is_authenticated:
            now = timezone.now()
            if user.last_password_reset_request and user.last_password_reset_request + cooldown_period > now:
                return HttpResponseForbidden("You have recently requested a password reset. Please wait for a minute before requesting another reset.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
