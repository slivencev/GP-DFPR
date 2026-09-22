from pathlib import Path
import json,hashlib,zipfile,shutil,unittest,io
root=Path(__file__).resolve().parent
old=root.parent/'GP_DFPR_Positioning_v13.zip'
with zipfile.ZipFile(old) as z:
    assert z.testzip() is None
    assert z.read('GP_DFPR_Positioning_v13/NOVELTY_AUDIT_RU.md')==(root.parent/'GP_DFPR_Positioning_v13/NOVELTY_AUDIT_RU.md').read_bytes()
(root/'V13_CHECKPOINT.json').write_text(json.dumps(dict(archive=old.name,sha256=hashlib.sha256(old.read_bytes()).hexdigest(),verified=True),indent=2))
shutil.copyfile(root.parent/'GP_DFPR_Validation_v2/results/colosseum_calibration.json',root/'EXISTING_EXTERNAL_CALIBRATION.json')
stream=io.StringIO();suite=unittest.defaultTestLoader.discover(str(root),pattern='test_evidence.py');result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);(root/'TESTS.txt').write_text(stream.getvalue());assert result.wasSuccessful()
(root/'MANIFEST.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'},indent=2))
dest=root.parent/'GP_DFPR_Observation_Model_v14.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for p in root.iterdir():
        if p.is_file():z.write(p,root.name+'/'+p.name)
with zipfile.ZipFile(dest) as z:assert z.testzip() is None
print(stream.getvalue());print('v13 verified; v14 package complete')
