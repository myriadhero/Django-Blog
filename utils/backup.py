import subprocess
import os
from datetime import datetime
from shutil import make_archive, rmtree

# Step 1: Create Backup Directory
backup_dir = os.path.expanduser(f"~/backups/blog_backup_{datetime.now().strftime('%Y%m%d_%H%MUTC')}")
os.makedirs(backup_dir, exist_ok=True)
print(f"{datetime.now()}: Backing up to {backup_dir}")

# Step 2: Backup Database
db_backup_command = f"docker compose --profile prod exec -t db pg_dumpall -c -U postgres > {backup_dir}/db_backup.sql"
subprocess.run(db_backup_command, shell=True, check=True)
print(f"{datetime.now()}: DB backup dumped")

# Step 3: Copy Media Files
media_backup_command = f"docker compose --profile prod cp web:/home/django/mediafiles/ {backup_dir}"
subprocess.run(media_backup_command, shell=True, check=True)
print(f"{datetime.now()}: Media Files dumped")

# Step 4: Archive
make_archive(backup_dir, "zip", backup_dir)
print(f"{datetime.now()}: Files archived")

# Step 5: Remove temp dir with unarchived files
rmtree(backup_dir)
print(f"{datetime.now()}: Temp files cleaned up")

# TODO: Step 6: Ecrypt
