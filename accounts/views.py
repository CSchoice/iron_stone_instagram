from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# 사용자 로그인 처리
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "잘못된 아이디 또는 비밀번호입니다."}, status=status.HTTP_401_UNAUTHORIZED)

# 사용자 로그아웃 처리
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)

# 회원정보 수정 페이지 조회
@api_view(['GET'])
def update_user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

#사용자 팔로우
def follow_user(request, tar_user_pk):
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