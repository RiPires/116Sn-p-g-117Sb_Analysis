import os
import uproot

files = [
    'data/AbsoluteEfficiency_HPGe_8mm_1e6.root',
    'data/AbsoluteEfficiency_HPGe_50mm_1e6.root',
    'data/AbsoluteEfficiency_HPGe_100mm_1e6.root',
]

for fpath in files:
    print('FILE', fpath)
    if not os.path.exists(fpath):
        print('MISSING')
        continue
    with uproot.open(fpath) as root_file:
        print('keys:', [k.name for k in root_file.keys()])
        for key in root_file.keys():
            obj = root_file[key.name]
            print(' ', key.name, type(obj).__name__, getattr(obj, 'classname', None))
            if hasattr(obj, 'keys'):
                try:
                    print('   subkeys', obj.keys())
                except Exception as exc:
                    print('   subkeys ERR', exc)
