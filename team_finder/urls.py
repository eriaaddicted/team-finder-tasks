from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from projects import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Списки проектов
    path('', project_views.project_list, name='index'),
    path('projects/list', project_views.project_list, name='project_list'),
    
    # Списки участников и профиль
    path('users/list', user_views.participants_list, name='participants_list'),
    path('users/<int:user_id>/', user_views.user_detail, name='user_detail'),
    
    # Роуты, которые запрашивает ваш фронтенд из skills.js
    path('projects/skills/', project_views.skill_autocomplete, name='skill_autocomplete'),
    path('projects/<int:project_id>/skills/add/', project_views.add_skill, name='add_skill'),
    path('projects/<int:project_id>/skills/<int:skill_id>/remove/', project_views.remove_skill, name='remove_skill'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)