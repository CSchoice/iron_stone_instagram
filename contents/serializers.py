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

class ArticleSerializerlike(serializers.ModelSerializer):
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'author', 'content', 'image', 'created_at', 'liked_by_user']

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_user.filter(pk=request.user.pk).exists()
        return False