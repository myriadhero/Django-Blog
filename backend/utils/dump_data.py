import os
import datetime

today = datetime.date.today()
filename = f"raw-data-{today.isoformat()}.json"
command = f"python -Xutf8 backend/manage.py dumpdata --all -o {filename}"

os.system(command)
