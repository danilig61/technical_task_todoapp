from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from todo_api.views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'folder-permissions', FolderPermissionViewSet, basename='folder-permissions')
router.register(r'page-permissions', PagePermissionViewSet, basename='page-permissions')
router.register(r'record-permissions', RecordPermissionViewSet, basename='record-permissions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('api/', include(router.urls)),
    path('api/v1/folder/', FolderViewSet.as_view(actions={'get': 'list'})),
    path('api/v1/folder/<int:pk>/', FolderViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy'}), name='folder-detail'),
    path('api/v1/pages/', PageViewSet.as_view(actions={'get': 'list'})),
    path('api/v1/pages/<int:pk>/', PageViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy'}), name='folder-detail'),
    path('api/v1/records/', RecordViewSet.as_view(actions={'get': 'list'})),
    path('api/v1/records/<int:pk>/', RecordViewSet.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy'}), name='folder-detail'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
