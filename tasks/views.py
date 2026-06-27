from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import filter_tasks
from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(
            user=request.user,
            deleted_at__isnull=True,
        )

        tasks = filter_tasks(tasks, request)

        return Response(
            {
                "message": "Tasks retrieved successfully.",
                "data": TaskSerializer(tasks, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = serializer.save(user=request.user)

        return Response(
            {
                "message": "Task created successfully.",
                "data": TaskSerializer(task).data,
            },
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_task(self, request, id):
        try:
            return Task.objects.get(
                id=id,
                user=request.user,
                deleted_at__isnull=True,
            )
        except Task.DoesNotExist:
            return None

    def get(self, request, id):
        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Task not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "message": "Task retrieved successfully.",
                "data": TaskSerializer(task).data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, id):
        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Task not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Task updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id):
        task = self._get_task(request, id)

        if task is None:
            return Response(
                {
                    "message": "Task not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        task.deleted_at = timezone.now()
        task.save()

        return Response(
            {
                "message": "Task deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )
