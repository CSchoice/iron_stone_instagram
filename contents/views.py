from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ArticleSerializer, CommentSerializer
from .models import Comment, Article
from accounts.models import User
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# DRF에서는 로그인 데코레이터를 사용하지 않음
# from django.contrib.auth.decorators import login_required


@swagger_auto_schema(
    method='get',
    operation_id='main_page',
    operation_description='메인 페이지를 조회합니다.',
    tags=['Article'],
    responses={200: openapi.Response(
        description="메인 페이지 조회 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="게시글 ID"),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용"),
                    # 추가적인 필드들을 여기에 정의할 수 있습니다.
                }
            )
        )
    )}
)
@api_view(['GET'])
def main_page(request):
    # 나와 팔로우 유저의 게시물 중 20개만 가져옮
    user_articles = Article.objects.filter(author=request.user)
    following_articles = Article.objects.filter(author__in=request.user.followings.all())
    articles = (user_articles | following_articles).order_by('-created_at')[:20]
    
    # serializer 작업
    serializer = ArticleSerializer(articles, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_id='user_profile',
    operation_description='특정 사용자의 프로필을 조회합니다.',
    tags=['User'],
    responses={200: openapi.Response(
        description="프로필 조회 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description="사용자 ID"),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="사용자명"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description="닉네임"),
                'introduce': openapi.Schema(type=openapi.TYPE_STRING, description="소개"),
                'followers_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="팔로워 수"),
                'followings_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="팔로잉 수"),
                'articles_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="게시글 수"),
                'articles': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="게시글 ID"),
                            'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
                            'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용"),
                            # 추가적인 필드들을 여기에 정의할 수 있습니다.
                        }
                    )
                ),
            }
        )
    )}
)
@api_view(['GET'])
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # 팔로우 수
    followers_count = user.followers.count()

    # 팔로잉 수
    followings_count = user.followings.count()

    # 게시글 수
    articles_count = user.article_set.count()

    # 사용자의 게시글들 조회
    articles = Article.objects.filter(author=user)
    serializer = ArticleSerializer(articles, many=True)

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


@swagger_auto_schema(
    method='get',
    operation_id='get_followers_list',
    operation_description='특정 사용자를 팔로우하는 사용자 목록을 조회합니다.',
    tags=['User'],
    responses={200: openapi.Response(
        description="팔로워 목록 조회 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="사용자 ID"),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description="사용자명"),
                }
            )
        )
    )}
)
# 특정 사용자를 팔로우하는 사용자 목록을 가져옮
@api_view(['GET'])
def get_followers_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    followers = user.followers.all()
    followers_list = []
    for follow in followers:
        followers_list.append({'id': follow.id, 'username': follow.username} )
    return Response(followers_list)


@swagger_auto_schema(
    method='get',
    operation_id='get_following_list',
    operation_description='특정 사용자가 팔로우하는 사용자 목록을 조회합니다.',
    tags=['User'],
    responses={200: openapi.Response(
        description="팔로잉 목록 조회 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="사용자 ID"),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description="사용자명"),
                }
            )
        )
    )}
)
# 특정 사용자가 팔로우하는 사용자 목록을 가져옮
@api_view(['GET'])
def get_following_list(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    following = user.following.all()
    following_list = []
    for follow in following:
        following_list.append({'id': follow.id, 'username': follow.username} )
    return Response(following_list)

# 게시글 작성
@swagger_auto_schema(
    method='post',
    operation_id='게시글 작성',
    operation_description='게시글을 작성합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용"),
        }
    ),
    tags=['게시글'],
    responses={201: openapi.Response(
        description="게시글 작성 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="게시글 ID"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용"),
                # 추가적인 필드들을 여기에 정의할 수 있습니다.
            }
        )
    )}
)
@api_view(['POST'])
def create_article(request):
    try:
        token_key = request.auth
        print(request.auth)
        print(request.user)
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
    
    if article.likes.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 한 경우, 좋아요 취소
        article.likes.remove(request.user)
        return Response({"message": "게시글 좋아요 취소"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        article.likes.add(request.user)
        return Response({"message": "게시글 좋아요 성공"}, status=status.HTTP_200_OK)