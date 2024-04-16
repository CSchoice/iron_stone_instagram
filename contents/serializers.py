from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Article
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'