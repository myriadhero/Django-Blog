import subprocess
import os
from datetime import datetime
from shutil import make_archive, rmtree
# from zipfile import ZipFile

# Step 1: Create Backup Directory
backup_dir = os.path.expanduser(f"~/backups/blog_backup_{datetime.now().strftime('%Y%m%d')}")
os.makedirs(backup_dir, exist_ok=True)

# Step 2: Backup Database
db_backup_command = f"docker compose --profile prod exec -t db pg_dumpall -c -U postgres > {backup_dir}/db_backup.sql"
subprocess.run(db_backup_command, shell=True, check=True)

# Step 3: Copy Media Files
media_backup_command = f"docker compose --profile prod cp web:/home/django/mediafiles/ {backup_dir}"
subprocess.run(media_backup_command, shell=True, check=True)

# Step 4: Archive
make_archive(backup_dir, "zip", backup_dir)

# TODO: Step 4.5: Password protect the zip

# Step 5: Remove Unprotected Files
rmtree(backup_dir)
