from .models import Task
from .serializers import TaskSerializer
import django.utils.timezone as timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import filter_tasks


class TaskView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tasks = Task.objects.filter(
            user=request.user,
            deleted_at__isnull=True
        )

        tasks = filter_tasks(tasks, request)

        if not tasks.exists():
            return Response(
                {
                    "message": "Nenhuma tarefa encontrada."
                },
                status=404
            )

        return Response(
            TaskSerializer(tasks, many=True).data
        )

    def post(self, request):

        serializer = TaskSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        task = serializer.save(user=request.user)

        return Response(
            TaskSerializer(task).data,
            status=201
        )


class TaskDetailView(APIView):
    def _get_task(self, request, id):
        try:
            task = Task.objects.get(
                id=id,
                user=request.user,
                deleted_at__isnull=True
            )
            return task

        except Task.DoesNotExist:
            return None

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Tarefa não encontrada."
                },
                status=404
            )

        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def patch(self, request, id):

        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Tarefa não encontrada."
                },
                status=404
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, id):

        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Tarefa não encontrada."
                },
                status=404
            )

        task.deleted_at = timezone.now()
        task.save()

        return Response(
            {
                "message": "Tarefa removida com sucesso."
            },
            status=200
        )
