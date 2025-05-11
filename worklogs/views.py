from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import StreamingHttpResponse
from django.db.models import Sum

from .models import WorkLog
from .serializers import WorkLogSerializer
from .permissions import IsWorkLogRoleBasedPermission
from core.filter import WorkLogFilter
from core.services.export_service import generate_worklog_csv, build_filename
from core.services.import_service import ImportMixin

class WorkLogViewSet(ImportMixin, ModelViewSet):
    queryset = WorkLog.objects.select_related('task__project', 'user').all()
    serializer_class = WorkLogSerializer
    model_serializer_class  = WorkLogSerializer
    permission_classes = [IsWorkLogRoleBasedPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkLogFilter

    @action(detail=False, methods=['get'], url_path='daily')
    def daily(self, request):
        if request.method == 'GET':
            queryset = (
                self.filter_queryset(self.get_queryset())
                .select_related('task__project', 'user')
            ).annotate(
                total_hours=Sum('spent_hours')
            ).order_by('work_date')
            
            response_data = [{
                    'email': row.user.email,
                    'work_date': row.work_date,
                    'total_hours': row.total_hours
                } for row in queryset
            ]
            return Response(response_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='daily/download')
    def daily_export(self, request):
        field_keys = ['user__email', 'work_date', 'total_hours']
        header = ['email', 'work_date', 'total_hours']
    
        queryset = (
            self.filter_queryset(self.get_queryset())
            .select_related('task__project', 'user')
        ).annotate(
            total_hours=Sum('spent_hours')
        ).order_by('work_date')
        
        data = [{
                'email': row.user.email,
                'work_date': row.work_date,
                'total_hours': row.total_hours,
            } for row in queryset
        ]
        
        excat = request.query_params.get('work_date_exact')
        if excat:
            filename = build_filename('report', excat)
        else:
            after = request.query_params.get('work_date_after')
            before = request.query_params.get('work_date_before')
            filename = build_filename('report', after, before)
        csv_generator = generate_worklog_csv(header, field_keys, data)

        response = StreamingHttpResponse(
            csv_generator,
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'},
        )
        return response
    
    @action(detail=False, methods=['get'], url_path='download')
    def export(self, request):
        field_keys = [
            'task__project__name', 'task__title',
            'user__email', 'work_date','spent_hours'
        ]
        header = [
            'project', 'title', 'email', 
            'work_date', 'spent_hours'
        ]
    
        queryset = (
            self.filter_queryset(self.get_queryset())
            .select_related('task__project', 'user')
        ).order_by('work_date')
        
        data = [{
                'project': row.task.project.name,
                'title': row.task.title,
                'email': row.user.email,
                'work_date': row.work_date,
                'spent_hours': row.spent_hours,
            } for row in queryset
        ]
        
        excat = request.query_params.get('work_date_exact')
        if excat:
            filename = build_filename('report', excat)
        else:
            after = request.query_params.get('work_date_after')
            before = request.query_params.get('work_date_before')
            filename = build_filename('report', after, before)
        csv_generator = generate_worklog_csv(header, field_keys, data)

        response = StreamingHttpResponse(
            csv_generator,
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'},
        )
        return response
