from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .serializers import LoginSerializer, UserSerializer


class UserView(CreateAPIView):
    authentication_classes = [TokenAuthentication]

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permition_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    def post(self, request: Request):
        login_validated = LoginSerializer(data=request.data)
        login_validated.is_valid(raise_exception=True)

        user = authenticate(**login_validated.validated_data)

        if not user:
            return Response(
                {"message": "Invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status.HTTP_201_CREATED)
