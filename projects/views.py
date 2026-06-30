from http import HTTPStatus
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from users.models import Skill
from .models import Project
from constants import SKILL_AUTOCOMPLETE_LIMIT, PROJECTS_PER_PAGE


def project_list(request):
    """Главная страница со списком проектов с защитой от N+1 и пагинацией."""
    projects_queryset = Project.objects.filter(
        status=Project.StatusChoices.OPEN
    ).select_related('author').prefetch_related('participants')
    
    paginator = Paginator(projects_queryset, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'projects/project_list.html', {'page_obj': page_obj})


@require_GET
def skill_autocomplete(request):
    """Поиск подсказок навыков."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    
    skills = Skill.objects.filter(name__icontains=query)[:SKILL_AUTOCOMPLETE_LIMIT]
    return JsonResponse([{'id': s.id, 'name': s.name} for s in skills], safe=False)


@login_required
@require_POST
def add_skill(request, project_id):
    """Добавление навыка текущему пользователю."""
    if request.user.id != int(project_id):
        return JsonResponse({'error': 'Доступ запрещен'}, status=HTTPStatus.FORBIDDEN)
        
    try:
        data = json.loads(request.body)
        skill_name = data.get('name', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Невалидный JSON'}, status=HTTPStatus.BAD_REQUEST)

    if not skill_name:
        return JsonResponse({'error': 'Имя навыка пустое'}, status=HTTPStatus.BAD_REQUEST)

    skill, created = Skill.objects.get_or_create(name=skill_name)
    request.user.skills.add(skill)
    return JsonResponse({'id': skill.id, 'name': skill.name}, status=HTTPStatus.OK)


@login_required
@require_POST
def remove_skill(request, project_id, skill_id):
    """Удаление навыка у пользователя."""
    if request.user.id != int(project_id):
        return JsonResponse({'error': 'Доступ запрещен'}, status=HTTPStatus.FORBIDDEN)
        
    skill = get_object_or_404(Skill, id=skill_id)
    request.user.skills.remove(skill)
    return JsonResponse({'success': True}, status=HTTPStatus.OK)