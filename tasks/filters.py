from .models import Task
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def filter_tasks(tasks, request):

    status = request.query_params.get("status")

    if not status:
        return tasks

    if status not in Task.Status.values:
        raise ValidationError(
            {
                "message": "Status inválido."
            }
        )

    return tasks.filter(status=status)
