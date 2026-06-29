import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from users.models import Skill
from .models import Project

def project_list(request):
    """Главная страница со списком проектов"""
    projects = Project.objects.filter(status='open')
    return render(request, 'projects/project_list.html', {'projects': projects})

# --- AJAX-обработчики под логику из skills.js ---

@require_GET
def skill_autocomplete(request):
    """Поиск подсказок навыков: /projects/skills/?q=..."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    skills = Skill.objects.filter(name__icontains=query)[:10]
    return JsonResponse([{'id': s.id, 'name': s.name} for s in skills], safe=False)

@login_required
@require_POST
def add_skill(request, project_id):
    """Добавление навыка к текущему юзеру: /projects/<id>/skills/add/"""
    if request.user.id != int(project_id):
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    body = json.loads(request.body)
    skill_id = body.get('skill_id')
    skill_name = body.get('name', '').strip()

    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    elif skill_name:
        skill, _ = Skill.objects.get_or_create(name=skill_name)
    else:
        return JsonResponse({'error': 'Данные пусты'}, status=400)

    request.user.skills.add(skill)
    return JsonResponse({'id': skill.id, 'name': skill.name})

@login_required
@require_POST
def remove_skill(request, project_id, skill_id):
    """Удаление навыка у юзера: /projects/<id>/skills/<id>/remove/"""
    if request.user.id != int(project_id):
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    
    skill = get_object_or_404(Skill, id=skill_id)
    request.user.skills.remove(skill)
    return JsonResponse({'status': 'success'})