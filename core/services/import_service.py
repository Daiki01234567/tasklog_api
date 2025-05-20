from rest_framework import status
from django.db import transaction
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core.exceptions import FieldError

from projects.models import Project
from tasks.models import Task
from projects.serializers import ProjectSerializer
from tasks.serializers import TaskSerializer
from worklogs.serializers import WorkLogSerializer
from core.serializers.file_upload import FileUploadSerializer
from core.utils import load_book, parse_int_or_none, normalize_df, require_columns

from pandas import DataFrame
from users.models import User
from typing import Any, List, Dict, Tuple, Type

def map_projects_from_dataframe(dataframe: DataFrame) -> List[Dict]:
    dataframe = normalize_df(dataframe)
    require_columns(dataframe, {'name'})
    
    mapped = [{
        'name': str(row.get('name', '')).strip(),
        'description': str(row.get('description', '')).strip()
        } for row in dataframe.to_dict(orient='records')
    ]
    return mapped

def map_tasks_from_dataframe(dataframe: DataFrame) -> List[Dict]:
    dataframe = normalize_df(dataframe)
    require_columns(dataframe, {'project_name', 'assignee_email'})

    try:
        names  = [str(x).strip() for x in dataframe['project_name'].dropna().unique().tolist()]
        emails = [str(x).strip() for x in dataframe['assignee_email'].dropna().unique().tolist()]
    except KeyError as e:
        raise ValidationError({'column': f'列参照エラー: {e.args[0]} が存在しません'}) 
    
    try:
        projects = Project.objects.filter(name__in=names).in_bulk(field_name='name')
        users = User.objects.filter(email__in=emails).in_bulk(field_name='email')
    except FieldError as e:
        raise ValidationError({'error': f'in_bulk の field_name エラー: {str(e)}'})
    
    mapped_list = []
    for row in dataframe.to_dict(orient='records'):
        project = projects.get(str(row.get('project_name', '')).strip())
        user = users.get(str(row.get('assignee_email', '')).strip())
        mapped = {
            'project': project.id if project else None,
            'title': str(row.get('title', '')).strip(),
            'planned_hours': parse_int_or_none(row.get('planned_hours', '')),
            'assignee': user.id if user else None,
            'due_date': str(row.get('due_date', '')).strip(),
            'status': str(row.get('status', '')).strip(),
        }
        mapped_list.append(mapped)
    return mapped_list

def map_worklogs_from_dataframe(dataframe: DataFrame) -> List[Dict]:
    dataframe = normalize_df(dataframe)
    require_columns(dataframe, {'title', 'email'})
    
    try:
        titles = [str(x).strip() for x in dataframe['title'].dropna().unique().tolist()]
        emails = [str(x).strip() for x in dataframe['email'].dropna().unique().tolist()]
    except KeyError as e:
        raise ValidationError({'error': f'列参照エラー: {e.args[0]} が存在しません'}) 

    task_queryset = Task.objects.filter(title__in=titles)
    task_map = { t.title: t for t in task_queryset }
    try:
        user_map = User.objects.filter(email__in=emails).in_bulk(field_name='email')
    except FieldError as e:
        raise ValidationError({'error': f'in_bulk の field_name エラー: {str(e)}'})

    mapped_list = []
    for row in dataframe.to_dict(orient='records'):
        task_obj = task_map.get(str(row.get('title', '')).strip())
        user_obj = user_map.get(str(row.get('email', '')).strip())
        mapped = {
            'task': task_obj.id if task_obj else None,
            'user': user_obj.id if user_obj else None,
            'spent_hours': parse_int_or_none(row.get('spent_hours', '')),
            'work_date': str(row.get('work_date', '')).strip(),
        }
        mapped_list.append(mapped)
    return mapped_list

ACTIONS = {
    ProjectSerializer: map_projects_from_dataframe,
    TaskSerializer: map_tasks_from_dataframe,
    WorkLogSerializer: map_worklogs_from_dataframe
}

def bulk_import_with_partial_errors(
        serializer_class: Type[Serializer],
        data_list: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], int]:
   
    created, errors = [], {}
    for idx, row in enumerate(data_list, start=1):
        serializer = serializer_class(data=row)
        if not serializer.is_valid():
            errors[idx] = [
                f"{field}: {','.join(msgs)}"
                for field, msgs in serializer.errors.items()
            ]
            continue
        created.append(serializer)

    if errors:
        return {
            'errors': errors,
        }, status.HTTP_400_BAD_REQUEST

    created_data = []
    with transaction.atomic():
        for seri in created:
            seri.save()
            created_data.append(seri.data)

    return {
        'created': created_data
    }, status.HTTP_201_CREATED

class ImportMixin:
    file_serializer_class = FileUploadSerializer
    model_serializer_class = None
    
    @action(detail=False,
            methods=['get', 'post'],
            url_path='import',
            serializer_class=FileUploadSerializer
    )
    def import_file(self, request):
        if request.method == 'GET':
            return Response(status=status.HTTP_200_OK)
        
        try:
            map_func = ACTIONS[self.model_serializer_class]
        except KeyError:
            raise ValueError(f'{self.model_serializer_class}用のマッピング関数が登録されていません。')
        
        serializer_upload = self.file_serializer_class(data=request.data)
        serializer_upload.is_valid(raise_exception=True)

        dataframe = load_book(serializer_upload.validated_data["file"])
        
        data_list = map_func(dataframe)
        
        data, status_code = bulk_import_with_partial_errors(
            self.model_serializer_class , data_list
        )
        
        return Response(data, status=status_code)
