from .models import Task
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def filter_tasks(tasks, request):

    status = request.query_params.get("status")
    title = request.query_params.get("title")

    if status and status not in Task.Status.values:
        raise ValidationError(
            {
                "message": "Status inválido."
            }
        )
    if status:
        tasks = tasks.filter(status=status)
    if title:
        tasks = tasks.filter(title__icontains=title)

    return tasks
