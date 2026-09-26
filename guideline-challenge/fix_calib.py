"""Fix calibration ZIPs: rename image stems to BDD sample_ids.
Schema: state values are [undefined, red, yellow, green, off, unknown] + needs_review checkbox.
Run this script every time a new zip is uploaded to keep sample_ids consistent.
"""
import csv
import io
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

CALIB_IDS = ['BDD01', 'BDD02', 'BDD03', 'BDD04', 'BDD05']
BASE = Path(__file__).parent
EXPORTS = BASE / 'project' / '06_calibration_exports'

# Map: zip stem -> original image stems in that zip
ZIP_STEM_MAP = {
    'my':   ['000000', '000001', '000002', '000003', '000004'],
    'dai':  ['000005', '000006', '000007', '000008', '000009'],
    'duan': ['000010', '000011', '000012', '000013', '000014'],
    'hung': ['000015', '000016', '000017', '000018', '000019'],
}


def rewrite_cvat_zip(zip_path: Path, old_stems: list, new_stems: list) -> None:
    """Rename <image name> stems in CVAT XML inside a zip, preserving all annotations."""
    z = zipfile.ZipFile(zip_path)
    members = [n for n in z.namelist() if Path(n).name == 'annotations.xml']
    if not members:
        print(f'[SKIP] {zip_path.name}: no annotations.xml found')
        z.close()
        return

    data = z.read(members[0]).decode('utf-8')
    z.close()

    root = ET.fromstring(data)
    renamed = 0
    for img in root.findall('image'):
        stem = Path(img.get('name', '')).stem
        if stem in old_stems:
            img.set('name', new_stems[old_stems.index(stem)] + '.jpg')
            renamed += 1

    decl = '<?xml version="1.0" encoding="utf-8"?>\n'
    new_xml = decl + ET.tostring(root, encoding='unicode')

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        zout.writestr('annotations.xml', new_xml.encode('utf-8'))
    zip_path.write_bytes(buf.getvalue())

    # Verify
    z2 = zipfile.ZipFile(zip_path)
    root2 = ET.fromstring(z2.read('annotations.xml'))
    imgs_after = [(img.get('name'), len(img.findall('box'))) for img in root2.findall('image')]
    print(f'[OK] {zip_path.name}: renamed {renamed} images -> {imgs_after}')


def rebuild_sample_pack() -> None:
    """Rebuild sample_pack.csv keeping non-calibration rows, ensuring calibration rows exist."""
    pack_path = BASE / 'project' / 'sample_pack.csv'
    existing = []
    if pack_path.exists():
        with open(pack_path, newline='', encoding='utf-8') as f:
            existing = [r for r in csv.DictReader(f) if r.get('split', '') != 'calibration']

    calib_rows = [
        {'sample_id': 'BDD01', 'split': 'calibration', 'tags': 'normal',
         'reason': 'traffic light daytime highway - baseline agreement check'},
        {'sample_id': 'BDD02', 'split': 'calibration', 'tags': 'normal',
         'reason': 'traffic light daytime city street - baseline agreement check'},
        {'sample_id': 'BDD03', 'split': 'calibration', 'tags': 'normal',
         'reason': 'traffic light overcast highway - baseline agreement check'},
        {'sample_id': 'BDD04', 'split': 'calibration', 'tags': 'edge',
         'reason': 'traffic light daytime city street - relevance ambiguity test'},
        {'sample_id': 'BDD05', 'split': 'calibration', 'tags': 'normal',
         'reason': 'traffic light daytime highway - count agreement check'},
    ]

    rows = calib_rows + existing
    with open(pack_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['sample_id', 'split', 'tags', 'reason'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'[OK] sample_pack.csv: {len(rows)} rows ({len(calib_rows)} calibration + {len(existing)} others)')


if __name__ == '__main__':
    for zip_name, old_stems in ZIP_STEM_MAP.items():
        zip_path = EXPORTS / (zip_name + '.zip')
        if not zip_path.exists():
            print(f'[SKIP] {zip_name}.zip not found')
            continue
        rewrite_cvat_zip(zip_path, old_stems, CALIB_IDS)

    rebuild_sample_pack()

    print('\nDone. Now run:')
    print('  $env:PYTHONUTF8=1; python lab9.py calib '
          'project/06_calibration_exports/dai.zip '
          'project/06_calibration_exports/my.zip '
          'project/06_calibration_exports/hung.zip '
          'project/06_calibration_exports/duan.zip')
