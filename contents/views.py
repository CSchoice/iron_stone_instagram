from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ArticleSerializer, CommentSerializer, ArticleSerializerlike
from .models import Comment, Article
from accounts.models import User
from rest_framework.authtoken.models import Token
# DRF에서는 로그인 데코레이터를 사용하지 않음
# from django.contrib.auth.decorators import login_required



@api_view(['GET'])
def main_page(request):
    # 나와 팔로우 유저의 게시물 중 20개만 가져옮
    user_articles = Article.objects.filter(author=request.user)
    following_articles = Article.objects.filter(author__in=request.user.followings.all())
    articles = (user_articles | following_articles).order_by('-created_at')[:20]
    
    # serializer 작업
    serializer = ArticleSerializer(articles, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_profile(request, tar_user_pk):
    user = get_object_or_404(User, id=tar_user_pk)

    # 팔로우 수
    followers_count = user.followers.count()

    # 팔로잉 수
    followings_count = user.followings.count()

    # 게시글 수
    articles_count = user.article_set.count()

    # 사용자의 게시글들 조회
    articles = Article.objects.filter(author=user)
    serializer = ArticleSerializerlike(articles, many=True, context={'request': request})


    profile_data = {
        'pk': user.pk,
        'username': user.username,
        'name': user.name,
        'nickname': user.nickname,
        'introduce': user.introduce,
        # 'profile_img': None,
        # 프로필 이미지 차후 추가 예정
        'followers_count': followers_count,
        'followings_count': followings_count,
        'articles_count': articles_count,
        'articles': serializer.data
    }

    return Response(profile_data, status=status.HTTP_200_OK)
# 특정 사용자를 팔로우하는 사용자 목록을 가져옮
@api_view(['GET'])
def get_followers_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    followers = user.followers.all()
    followers_list = []
    for follow in followers:
        followers_list.append({'id': follow.id, 'username': follow.username} )
    return Response(followers_list)

# 특정 사용자가 팔로우하는 사용자 목록을 가져옮
@api_view(['GET'])
def get_following_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    following = user.following.all()
    following_list = []
    for follow in following:
        following_list.append({'id': follow.id, 'username': follow.username} )
    return Response(following_list)

# 게시글 작성
@api_view(['POST'])
def create_article(request):
    try:
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response({'error': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 정보 조회
@api_view(['GET'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 게시글 수정, 삭제
@api_view(['PUT', 'DELETE'])
def edit_article(request, article_pk):
    if request.method == 'PUT':
        article = Article.objects.get(pk=article_pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'DELETE':
        article = Article.objects.get(pk=article_pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 작성
@api_view(['POST'])
def create_comment(request, article_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(article_id=article_pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정, 삭제
@api_view(['PUT', 'DELETE'])
def edit_comment(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    serializer = CommentSerializer(comment, data=request.data)
    if request.method == 'PUT':
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def like_article(request, article_pk):
    if not request.user.is_authenticated:
        return Response({"message": "로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
    
    article = get_object_or_404(Article, pk=article_pk)
    
    if article.like_user.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 한 경우, 좋아요 취소
        article.like_user.remove(request.user)
        return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        article.like_user.add(request.user)
        return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)