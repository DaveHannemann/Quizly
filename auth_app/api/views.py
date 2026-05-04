from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegistrationView(APIView):
    """
    Handles user registration.

    Accepts user data (e.g. username, email, password),
    validates it via RegistrationSerializer, and creates a new user.
    """
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response({'detail': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Authenticates a user and issues JWT tokens via HTTP-only cookies.

    Overrides the default TokenObtainPairView to:
        - Return user information
        - Store access and refresh tokens in cookies instead of response body

    Cookies:
        - access_token (short-lived)
        - refresh_token (long-lived)
    """

    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            data = {
                'id': serializer.user.id,
                'username': serializer.user.username,
                'email': serializer.user.email
            }

            refresh = serializer.validated_data["refresh"]
            access = serializer.validated_data["access"]

            response = Response({"detail": "Login successfully!", 'user': data})

            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=True,
                samesite="Lax"
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax"
            )

            return response
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    """
    Logs out the authenticated user by removing JWT cookies.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    """
    Refreshes the access token using the refresh token stored in cookies.

    Overrides the default TokenRefreshView to:
        - Read refresh token from HTTP-only cookie
        - Generate a new access token and update cookie
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"detail": "Refresh token not provided or missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail": "Refresh token not provided or missing"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get("access")

        response = Response({"detail": "Token refreshed successfully!"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response