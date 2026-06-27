from .models import Task
from .serializers import TaskSerializer

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

        taks = serializer.save(user=request.user)

        return Response(
            TaskSerializer(taks).data,
            status=201
        )
