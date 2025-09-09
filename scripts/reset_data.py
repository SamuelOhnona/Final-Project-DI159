import os, glob
BASE = 'campaigns'
files = [
    os.path.join(BASE, 'simulated_ads.csv'),
    os.path.join(BASE, 'prompts_log.csv'),
    *glob.glob(os.path.join(BASE, 'categories', '*.csv')),
]
for f in files:
    if os.path.exists(f):
        os.remove(f)
print('✔ Data reset: removed simulated CSV files.')
