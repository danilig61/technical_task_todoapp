import logging

from rest_framework import viewsets, permissions, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info('Пользователь зарегистрирован: %s', user.username)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        logger.info('Пользователь вошел в систему: %s', user.username)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        folder = serializer.save(owner=self.request.user)
        logger.info('Папка создана: ID пользователя %s, ID записи %s', self.request.user.id, folder.id)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        page = serializer.save(user=self.request.user)
        logger.info('Страница создана: ID пользователя %s, ID записи %s', self.request.user.id, page.id)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        record = serializer.save(user=self.request.user)
        logger.info('Запись создана: ID пользователя %s, ID записи %s', self.request.user.id, record.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        logger.info('Запись удалена: ID пользователя %s, ID записи %s', self.request.user.id, instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)




class FolderPermissionViewSet(viewsets.ModelViewSet):
    queryset = FolderPermission.objects.all()
    serializer_class = FolderPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        permission = serializer.save()
        logger.info('Разрешение на папку создано: ID пользователя %s, ID записи %s', self.request.user.id,
                    permission.id)


class PagePermissionViewSet(viewsets.ModelViewSet):
    queryset = PagePermission.objects.all()
    serializer_class = PagePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        permission = serializer.save()
        logger.info('Разрешение на страницу создано: ID пользователя %s, ID записи %s', self.request.user.id,
                    permission.id)


class RecordPermissionViewSet(viewsets.ModelViewSet):
    queryset = RecordPermission.objects.all()
    serializer_class = RecordPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        permission = serializer.save()
        logger.info('Разрешение на запись создано: ID пользователя %s, ID записи %s', self.request.user.id,
                    permission.id)
