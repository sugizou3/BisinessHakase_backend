from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet, basename='profile')
router.register('posts', views.PostViewSet, basename='posts')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('detail-post/<str:pk>', views.PostRetrieveView.as_view(), name='detail-post'),
    path('list-post/<str:pk>', views.PostListView.as_view(), name='list-post'),
    path('auth/', include('djoser.urls.jwt')),
    path('',include(router.urls))
]