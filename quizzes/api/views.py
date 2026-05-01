from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizzes.models import Quiz
from .serializers import QuizSerializer

from quizzes.services.pipeline_service import create_quiz

import traceback

class QuizzesView(APIView):

    def get(self, request):
        quizzes = Quiz.objects.all().order_by("-created_at")
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response({"error": "URL required"}, status=400)

        try:
            quiz_data = create_quiz(url)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": "Failed to create quiz"}, status=500)
        
        quiz = Quiz.objects.create(
            title=quiz_data.get("title"),
            description=quiz_data.get("description"),
            video_url=url,
            questions=quiz_data.get("questions")
        )

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=201)