from .base import *  # noqa

DEBUG = True

# Dev'da Celery worker shart emas: vazifalar so'rov ichida darrov bajariladi.
# Prod'da bu o'chiq, import alohida worker'da ishlaydi.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = False