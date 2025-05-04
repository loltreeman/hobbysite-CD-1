from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('profile/edit/', views.profile_update, name='profile_update'),
    path('signup/', views.register_view, name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
app_name = 'user_management'