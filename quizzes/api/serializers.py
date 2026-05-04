from rest_framework import serializers
from quizzes.models import Quiz


class QuizCreateSerializer(serializers.Serializer):
    video_url = serializers.URLField()

    def validate_video_url(self, value):
        if not value:
            raise serializers.ValidationError("URL erforderlich")
        return value

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']

class QuizUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating quiz metadata.

    Restricts updates strictly to allowed fields and rejects
    any unexpected input fields.

    Allowed fields:
        - title
        - description
    """
    
    class Meta:
        model = Quiz
        fields = ['title', 'description']

    def validate(self, data):
        incoming_fields = set(self.initial_data.keys())
        allowed_fields = set(self.fields.keys())
        invalid_fields = incoming_fields - allowed_fields
        
        if invalid_fields:
            raise serializers.ValidationError(
                f"Invalid fields: {', '.join(invalid_fields)}"
            )
        return data