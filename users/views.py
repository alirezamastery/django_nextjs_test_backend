from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .serializers import CustomUserSerializer, CustomUserDetailSerializer, TestUser, LoginSerializer


User = get_user_model()


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.save()
            if user_obj:
                json = serializer.data
                refresh = RefreshToken.for_user(user_obj)
                print(f'token: {refresh} | refresh.access_token: {refresh.access_token}')
                # TODO also return a token for login after sign up
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.data
        serializer = CustomUserSerializer(data=user)
        if serializer.is_valid():
            print('validated data:', serializer.validated_data)

        return Response(request.data)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            # print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            # print('token: ' ,token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TestUserDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        send request with a valid token to get user data
        :param request: 'username' , 'password'
        :return: user object
        """
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username:
            try:
                user_obj = User.objects.get(username=username, password=password)
            except User.DoesNotExist:
                return Response(data='wrong credentials', status=status.HTTP_400_BAD_REQUEST)
        data = {
            'user':         TestUser(user_obj).data,
            'other things': 'other things for you'
        }

        return Response(data)


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'user':    TestUser(user, context=self.get_serializer_context()).data,
                'refresh': str(refresh),
                'access':  str(refresh.access_token),
            })
