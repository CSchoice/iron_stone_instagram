from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated



# 사용자 로그인 처리
class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_json = UserSerializer(user).data

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": user_json,
            }
        )


# 사용자 로그아웃 처리
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)

# 회원정보 수정 페이지 조회
@api_view(['GET', 'POST'])
def update_user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        #get 요청 처리
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        if request.user.pk != user.pk:
            # 로그인한 유저와, 해당 회원정보 유저가 다른 경우
            return Response({"message": "자신의 정보만 수정할 수 있습니다"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            #정상적으로 수정
            return Response(serializer.data, status=status.HTTP_200_OK)
            #형식이 맞지 않음
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#사용자 팔로우
@api_view(['POST'])
def follow_user(request, tar_user_pk):
    try:
        token_key = request.auth
        token = Token.objects.get(key=token_key)
        # user = token.user
    except Token.DoesNotExist:
        return Response({'error': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    target_user = get_object_or_404(User, pk=tar_user_pk)
    if request.user.is_authenticated:
        if request.user.followings.filter(pk=tar_user_pk).exists():
            # 이미 팔로우한 상태면 언팔로우
            request.user.followings.remove(target_user)
            return Response({"message": "언팔로우 성공"}, status=status.HTTP_200_OK)
        else:
            # 아직 팔로우하지 않은 상태면 팔로우
            request.user.followings.add(target_user)
            return Response({"message": "팔로우 성공"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_login(request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)