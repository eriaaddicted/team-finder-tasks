from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Skill

User = get_user_model()

def participants_list(request):
    """Список участников с фильтрацией по тегам навыков"""
    all_skills = Skill.objects.filter(users__isnull=False).distinct().order_by('name')
    active_skill_name = request.GET.get('skill', '').strip()
    
    participants = User.objects.filter(is_active=True).order_by('-date_joined')
    
    if active_skill_name:
        participants = participants.filter(skills__name=active_skill_name)
    
    if request.user.is_authenticated:
        participants = participants.exclude(id=request.user.id)

    context = {
        'participants': participants,
        'all_skills': all_skills,
        'active_filter': active_skill_name,
    }
    return render(request, 'users/participants.html', context)

def user_detail(request, user_id):
    """Страница профиля"""
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': user_obj})