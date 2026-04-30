from django.urls import path
from .views import QuizzesView

urlpatterns = [
    path('quizzes/', QuizzesView.as_view(), name='quizzes'),
    # path('quizzes/<int:quiz_id>/', SingleQuizView.as_view(), name='single-quiz'),
]