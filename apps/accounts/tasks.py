import structlog
from django.core.mail import send_mail
from django_tasks import TaskContext, task

from .models import User

logger = structlog.get_logger(__name__)


@task(queue_name="emails", priority=50, takes_context=True)
def send_welcome_email(context: TaskContext, user_id: str) -> dict:
    """
    Background task to send welcome email to a newly registered user.
    Uses PostgreSQL task queue.
    """
    logger.info("Processing send_welcome_email task", user_id=user_id, attempt=context.attempt)
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject="Welcome to Ready-to-Go Django!",
            message=f"Hello {user.username},\n\nWelcome to your new modern Django application.",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("Welcome email sent successfully", user_id=user_id)
        return {"status": "sent", "user_id": user_id}
    except User.DoesNotExist:
        logger.warning("User not found for welcome email", user_id=user_id)
        return {"status": "not_found", "user_id": user_id}
    except Exception as exc:
        logger.error("Failed to send welcome email", error=str(exc), user_id=user_id)
        raise
