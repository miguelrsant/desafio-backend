from .models import Task
from .serializers import TaskSerializer
import django.utils.timezone as timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TaskView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        tasks = Task.objects.filter(
            user=user,
            deleted_at__isnull=True
        )

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

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        try:
            task = Task.objects.get(
                id=id,
                user=request.user,
                deleted_at__isnull=True
            )

        except Task.DoesNotExist:
            return Response(
                {
                    "message": "Tarefa não encontrada."
                },
                status=404
            )

        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def patch(self, request, id):

        try:
            task = Task.objects.get(
                id=id,
                user=request.user,
                deleted_at__isnull=True
            )

        except Task.DoesNotExist:
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

        try:
            task = Task.objects.get(
                id=id,
                user=request.user,
                deleted_at__isnull=True
            )

        except Task.DoesNotExist:
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
