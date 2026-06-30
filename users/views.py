from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Skill
from constants import PARTICIPANTS_PER_PAGE

User = get_user_model()


def participants_list(request):
    """Список участников с фильтрацией по навыкам и пагинацией."""
    all_skills = Skill.objects.filter(users__isnull=False).distinct()
    active_skill_name = request.GET.get('skill', '').strip()
    
    participants_queryset = User.objects.filter(is_active=True)
    
    if active_skill_name:
        participants_queryset = participants_queryset.filter(skills__name=active_skill_name)
        
    if request.user.is_authenticated:
        participants_queryset = participants_queryset.exclude(id=request.user.id)
        
    paginator = Paginator(participants_queryset, PARTICIPANTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'all_skills': all_skills,
        'active_filter': active_skill_name,
    }
    
    return render(request, 'users/participants.html', context)


def user_detail(request, user_id):
    """Детальная страница пользователя."""
    user = get_object_or_404(User, id=user_id, is_active=True)
    return render(request, 'users/user_detail.html', {'user_obj': user})