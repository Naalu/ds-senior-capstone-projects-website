from .models import Notification


def unread_notifications(request):
    """Makes unread notifications available to templates."""
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        unread_count = notifications.count()
        # Limit the number shown in dropdown for performance/UI reasons
        recent_unread = notifications[:5]
    else:
        unread_count = 0
        recent_unread = []

    return {
        "unread_notifications_count": unread_count,
        "recent_unread_notifications": recent_unread,
    }
