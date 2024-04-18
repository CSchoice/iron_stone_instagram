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

# class ArticleSerializerlike(serializers.ModelSerializer):
#     liked_by_user = serializers.SerializerMethodField()

#     class Meta:
#         model = Article
#         fields = ['id', 'author', 'content', 'image', 'created_at','updated_at', 'liked_by_user']

#     def get_liked_by_user(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return obj.like_user.filter(pk=request.user.pk).exists()
#         return False
    
class Article_like_comment_Serializer(serializers.ModelSerializer):
    liked_by_user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'author', 'content', 'image', 'created_at', 'updated_at', 'liked_by_user', 'comments', 'likes_count']
    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_user.filter(pk=request.user.pk).exists()
        return False

    def get_comments(self, obj):
        # 해당 게시물에 대한 댓글들 가져오기
        comments = Comment.objects.filter(article=obj)
        # 댓글들을 CommentSerializer를 사용하여 시리얼라이즈
        comment_serializer = CommentSerializer(comments, many=True)
        return comment_serializer.data
    
    def get_likes_count(self, obj):
        return obj.like_user.count()