from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizzes.models import Quiz

from quizzes.services.pipeline_service import create_quiz

import traceback

class QuizzesView(APIView):

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

        return Response({
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "video_url": quiz.video_url,
            "questions": quiz.questions
        }, status=201)