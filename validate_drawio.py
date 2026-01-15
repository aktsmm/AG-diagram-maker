import xml.etree.ElementTree as ET
import os

files = [
    'outputs/application-form-system-overview.drawio',
    'outputs/application-form-system-detailed.drawio'
]

os.chdir('d:/03_github/Ag-diagram-maker')

for f in files:
    print(f'=== {os.path.basename(f)} ===')
    tree = ET.parse(f)
    root = tree.getroot()
    
    # mxfile属性チェック
    gen = root.get('generator', 'なし')
    print(f'generator: {gen}')
    
    # mxCellカウント
    cells = root.findall('.//mxCell')
    vertices = len([c for c in cells if c.get('vertex') == '1'])
    edges = len([c for c in cells if c.get('edge') == '1'])
    ids = [c.get('id') for c in cells]
    
    print(f'mxCell総数: {len(cells)}')
    print(f'  - vertex: {vertices}')
    print(f'  - edge: {edges}')
    
    has_root = '0' in ids and '1' in ids
    status = 'OK' if has_root else 'NG'
    print(f'ルートセル(0,1): {status}')
    print()
