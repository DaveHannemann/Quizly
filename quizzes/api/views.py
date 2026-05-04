from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizzes.api.permissions import IsAdminOrQuizCreator
from quizzes.models import Quiz
from .serializers import QuizCreateSerializer, QuizSerializer, QuizUpdateSerializer

from quizzes.services.pipeline_service import create_quiz

import traceback

class QuizzesView(APIView):
    """
    Handles listing and creation of quizzes.

    Permissions:
        - Admin users can access all quizzes
        - Regular users can only access their own quizzes
    """
    permission_classes = [IsAdminOrQuizCreator]

    def get(self, request):
        if request.user.is_staff:
            quizzes = Quiz.objects.all().order_by("-created_at")
        else:
            quizzes = Quiz.objects.filter(created_by=request.user).order_by("-created_at")
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new quiz from a provided video URL.

        Flow:
            1. Normalize input (map "url" → "video_url")
            2. Validate input via QuizCreateSerializer
            3. Process video via create_quiz service
            4. Store generated quiz in database
        """

        data = request.data.copy()
        data["video_url"] = data.pop("url", None)

        serializer = QuizCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        url = serializer.validated_data["video_url"]

        if not url:
            return Response({"error": "URL required"}, status=400)

        try:
            quiz_data = create_quiz(url)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except Exception:
            traceback.print_exc()
            return Response({"error": "Failed to create quiz"}, status=500)
        
        quiz = Quiz.objects.create(
            title=quiz_data.get("title"),
            description=quiz_data.get("description"),
            video_url=url,
            questions=quiz_data.get("questions"),
            created_by=request.user
        )

        return Response(QuizSerializer(quiz).data, status=201)
    

class SingleQuizView(APIView):
    permission_classes = [IsAdminOrQuizCreator]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        self.check_object_permissions(request, quiz)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    
    def patch(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        self.check_object_permissions(request, quiz)

        serializer = QuizUpdateSerializer(quiz, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()

        return Response(QuizSerializer(quiz).data)
    
    def delete(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        self.check_object_permissions(request, quiz)

        quiz.delete()
        return Response({"detail": "Quiz deleted successfully"}, status=204)