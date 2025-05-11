import csv
from typing import Optional, Any, Generator, List, Dict

class Echo:
    """csv.writer のための擬似バッファ。write() は値をそのまま返すだけ。"""
    def write(self, value):
        return value

def build_filename(
    name: str,
    start: Optional[str] = None,
    end: Optional[str] = None) -> str:

    if start and end and start == end:
        name += f'_{start}'
    if start:
        name += f'_from-{start}'
    if end:
        name += f'_to-{end}'
    return name + '.csv'

def generate_worklog_csv(
    header: List[str],
    field_keys: List[str],
    rows: List[Dict[str, Any]]) -> Generator[str, None, None]:
    
    pseudo_buffer = Echo()
    writer = csv.writer(
        pseudo_buffer,
        quoting=csv.QUOTE_ALL,
        doublequote=True,
        quotechar='"',
        delimiter=',',
        escapechar='\\',
        lineterminator='\r\n'
    )
    
    yield writer.writerow([h for h in header])
    
    for item in rows:
        yield writer.writerow([item.get(key, "") for key in field_keys])
