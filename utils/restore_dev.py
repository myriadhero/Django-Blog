import argparse
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

# Constants for default paths
DEFAULT_BACKUP_FOLDER = Path.home() / "backups"
MEDIAFILES_DIR = "mediafiles/"
LOCAL_MEDIAFILES_PATH = Path("backend") / "media"
DOCKER_MEDIAFILES_PATH = "/home/django/mediafiles/"
DB_BACKUP_FILENAME = "db_backup.sql"


def get_latest_zip(default_folder: Path) -> Path | None:
    """Find the most recently modified .zip file in the default folder."""
    if not default_folder.exists():
        return None
    zip_files = [f for f in default_folder.iterdir() if f.is_file() and f.suffix == ".zip"]
    if not zip_files:
        return None
    return max(zip_files, key=lambda f: f.stat().st_mtime)


def restore_backup(zip_path: Path, db_only: bool = False, prod: bool = False):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        profile = "prod" if prod else "dev"
        docker_db_service = "db-dev" if profile == "dev" else "db"

        # Check for required files
        zip_contents = zip_ref.namelist()
        has_db_backup = DB_BACKUP_FILENAME in zip_contents
        has_mediafiles = any(name.startswith(MEDIAFILES_DIR) for name in zip_contents)

        # Step 1: Restore database
        if has_db_backup:
            # Extract db_backup.sql to a temporary file
            with tempfile.NamedTemporaryFile(delete_on_close=False, suffix=".sql") as temp_sql:
                temp_sql.write(zip_ref.read(DB_BACKUP_FILENAME))
                temp_sql.close()

                db_restore_command = f"cat {temp_sql.name} | docker compose --profile {profile} exec -T {docker_db_service} psql -U postgres"
                subprocess.run(db_restore_command, shell=True, check=True)
                print(f"{datetime.now()}: Database restored")

        else:
            print(f"{datetime.now()}: Warning: {DB_BACKUP_FILENAME} not found in backup")

        # Step 2: Restore media files (if not db-only)
        if not db_only and has_mediafiles:
            # Create a temporary directory for media files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                # Extract mediafiles/ directory to temp_dir
                for item in zip_contents:
                    if item.startswith(MEDIAFILES_DIR) and not item.endswith("/"):
                        # Extract file to temp_dir, preserving the mediafiles/ structure
                        rel_path = item[len(MEDIAFILES_DIR) :]
                        target_path = temp_dir_path / MEDIAFILES_DIR / rel_path
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with target_path.open("wb") as f:
                            f.write(zip_ref.read(item))

                temp_mediafiles_path = temp_dir_path / MEDIAFILES_DIR
                if profile == "prod":
                    # Copy media files to Docker container with prod profile
                    media_restore_command = (
                        f"docker compose --profile {profile} cp {temp_mediafiles_path}/. web:{DOCKER_MEDIAFILES_PATH}"
                    )
                    subprocess.run(media_restore_command, shell=True, check=True)
                    print(
                        f"{datetime.now()}: Media files restored to Docker at {DOCKER_MEDIAFILES_PATH} (profile: {profile})",
                    )
                else:
                    # Copy media files to local folder, overwriting existing files
                    if LOCAL_MEDIAFILES_PATH.exists():
                        shutil.rmtree(LOCAL_MEDIAFILES_PATH)
                    shutil.copytree(temp_mediafiles_path, LOCAL_MEDIAFILES_PATH)
                    print(f"{datetime.now()}: Media files copied to local folder {LOCAL_MEDIAFILES_PATH}")
        elif not db_only and not has_mediafiles:
            print(f"{datetime.now()}: Warning: {MEDIAFILES_DIR} directory not found in backup")

    print(f"{datetime.now()}: Restoration complete")


def main():
    parser = argparse.ArgumentParser(description="Restore Django backup to dev environment")
    parser.add_argument(
        "zip_path",
        type=Path,
        nargs="?",
        help=f"Path to the backup .zip file (optional; uses latest in {DEFAULT_BACKUP_FOLDER} if not provided)",
    )
    parser.add_argument("--db", action="store_true", help="Restore only the database")
    parser.add_argument(
        "--prod",
        action="store_true",
        help=f"Push media files to Docker ({DOCKER_MEDIAFILES_PATH}, profile: prod) instead of copying to local folder ({LOCAL_MEDIAFILES_PATH})",
    )
    args = parser.parse_args()

    if args.zip_path is None:
        zip_path = get_latest_zip(DEFAULT_BACKUP_FOLDER)
        if zip_path is None:
            print(f"Error: No .zip files found in {DEFAULT_BACKUP_FOLDER}")
            return
        print(f"{datetime.now()}: Using latest backup: {zip_path}")
    else:
        zip_path = args.zip_path

    if not zip_path.exists():
        print(f"Error: Backup file {zip_path} does not exist")
        return

    restore_backup(zip_path, db_only=args.db, prod=args.prod)


if __name__ == "__main__":
    main()
