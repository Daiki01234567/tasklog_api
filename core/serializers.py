from rest_framework import serializers

import magic
from pathlib import Path

MAX_SIZE = 10 * 1024 * 1024
MAX_LINES = 50000

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        max_size = MAX_SIZE
        if value.size > max_size:
            raise serializers.ValidationError('ファイルサイズは10MB以内にしてください。')
        
        ext = Path(value.name).suffix.lower()
        if ext not in ['.csv', '.xlsx']:
            raise serializers.ValidationError('CSVかExcelファイルのみアップロード可能です。')
    
        head = value.read(2048)
        mime = magic.from_buffer(head, mime=True)
        value.seek(0)
        allowed_mimes = {
            '.csv': ['text/csv', 'application/csv', 'text/plain'],
            '.xlsx': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
        }
        if mime not in allowed_mimes[ext]:
            raise serializers.ValidationError(f'MIMEタイプが不正です: {mime}')

        head8 = value.read(8)
        value.seek(0)
        if ext == '.xlsx':
            if not head8.startswith(b'PK\x03\x04'):
                raise serializers.ValidationError('XLSXファイルではありません。')
        else:
            if head8.startswith(b'\xef\xbb\xbf'):
                import logging
                logging.warning('UTF-8 BOM が検出されました。')
        
        lines = value.read().splitlines()
        value.seek(0)
        if len(lines) > MAX_LINES:
            raise serializers.ValidationError(f'ファイルは{MAX_LINES}行以内にしてください。')
        return value