# # backup.py - A Python script to create a backup of a PostgreSQL database and encrypt it using OpenSSL.
# import os
# import subprocess
# from datetime import datetime, timedelta
# import shutil

# def create_backup():
#     # Load environment variables
#     DB_HOST = os.getenv('DB_HOST', 'localhost')
#     DB_PORT = os.getenv('DB_PORT', '5432')
#     DB_USER = os.getenv('DB_USER', 'postgres')
#     DB_PASS = os.getenv('DB_PASS', 'password')
#     DB_NAME = os.getenv('DB_NAME', 'postgres')
#     BACKUP_DIR = os.getenv('BACKUP_DIR', '/mnt/backups')
#     RETENTION_DAYS = int(os.getenv('RETENTION_DAYS', '7'))
#     ENCRYPTION_PASSWORD = os.getenv('ENCRYPTION_PASSWORD', 'passwordencryption')

#     # Create a timestamp for the backup
#     timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
#     backup_file = os.path.join(BACKUP_DIR, f"bica-backup-{timestamp}.tar.gz")

#     # Set the PGPASSWORD environment variable for pg_dump
#     os.environ['PGPASSWORD'] = DB_PASS

#     # Create the backup using pg_dump and gzip
#     print("Creating backup...")
#     with open(backup_file, 'wb') as f_out:
#         try:
#             dump_command = [
#                 'pg_dump',
#                 '-h', DB_HOST,
#                 '-p', DB_PORT,
#                 '-U', DB_USER,
#                 DB_NAME
#             ]
#             dump_process = subprocess.Popen(dump_command, stdout=subprocess.PIPE)
#             gzip_process = subprocess.Popen(['gzip'], stdin=dump_process.stdout, stdout=f_out)
#             dump_process.stdout.close()  # Allow dump_process to receive a SIGPIPE if gzip_process exits.
#             gzip_process.communicate()

#             if gzip_process.returncode == 0:
#                 print(f"Backup created: {backup_file}")
#             else:
#                 print("Error: pg_dump failed.")
#                 return False
#         except Exception as e:
#             print(f"Error during backup creation: {e}")
#             return False
#         finally:
#             # Unset the PGPASSWORD environment variable
#             del os.environ['PGPASSWORD']

#     # Encrypt the backup file
#     encrypted_file = f"{backup_file}.enc"
#     print("Encrypting backup...")
#     try:
#         encryption_command = [
#             'openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt',
#             '-in', backup_file,
#             '-out', encrypted_file,
#             '-k', ENCRYPTION_PASSWORD
#         ]
#         subprocess.run(encryption_command, check=True)
#         print(f"Encryption successful: {encrypted_file}")

#         # Remove the unencrypted backup file
#         os.remove(backup_file)
#     except subprocess.CalledProcessError as e:
#         print(f"Error: Encryption failed: {e}")
#         os.remove(backup_file)
#         return False

#     # Remove backups older than retention days
#     print("Removing old backups...")
#     cleanup_old_backups(BACKUP_DIR, RETENTION_DAYS)

#     print("Backup completed successfully.")
#     return True

# def cleanup_old_backups(backup_dir, retention_days):
#     now = datetime.now()
#     for filename in os.listdir(backup_dir):
#         if filename.endswith(".tar.gz.enc"):
#             file_path = os.path.join(backup_dir, filename)
#             file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
#             if now - file_mtime > timedelta(days=retention_days):
#                 os.remove(file_path)
#                 print(f"Removed old backup: {file_path}")

# def main():
#     if not create_backup():
#         print("Backup failed.")

# if __name__ == '__main__':
#     main()

import os
import subprocess
from datetime import datetime, timedelta

def create_backup():
    # Load environment variables
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'password')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    BACKUP_DIR = os.getenv('BACKUP_DIR', '/mnt/backups')
    RETENTION_DAYS = int(os.getenv('RETENTION_DAYS', '7'))
    ENCRYPTION_PASSWORD = os.getenv('ENCRYPTION_PASSWORD', 'passwordencryption')

    # Ensure the backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Create a timestamp for the backup
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    backup_file = os.path.join(BACKUP_DIR, f"bica-backup-{timestamp}.tar.gz")

    # Set the PGPASSWORD environment variable for pg_dump
    os.environ['PGPASSWORD'] = DB_PASS

    # Create the backup using pg_dump and gzip
    print("Creating backup...")
    with open(backup_file, 'wb') as f_out:
        try:
            dump_command = [
                'pg_dump',
                '-h', DB_HOST,
                '-p', DB_PORT,
                '-U', DB_USER,
                DB_NAME
            ]
            dump_process = subprocess.Popen(dump_command, stdout=subprocess.PIPE)
            gzip_process = subprocess.Popen(['gzip'], stdin=dump_process.stdout, stdout=f_out)
            dump_process.stdout.close()  # Allow dump_process to receive a SIGPIPE if gzip_process exits.
            gzip_process.communicate()

            if gzip_process.returncode == 0:
                print(f"Backup created: {backup_file}")
            else:
                print("Error: pg_dump failed.")
                return False
        except Exception as e:
            print(f"Error during backup creation: {e}")
            return False
        finally:
            # Unset the PGPASSWORD environment variable
            del os.environ['PGPASSWORD']

    # Encrypt the backup file
    encrypted_file = f"{backup_file}.enc"
    print("Encrypting backup...")
    try:
        encryption_command = [
            'openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt',
            '-in', backup_file,
            '-out', encrypted_file,
            '-k', ENCRYPTION_PASSWORD
        ]
        subprocess.run(encryption_command, check=True)
        print(f"Encryption successful: {encrypted_file}")

        # Remove the unencrypted backup file
        os.remove(backup_file)
    except subprocess.CalledProcessError as e:
        print(f"Error: Encryption failed: {e}")
        os.remove(backup_file)
        return False

    # Remove backups older than retention days
    print("Removing old backups...")
    cleanup_old_backups(BACKUP_DIR, RETENTION_DAYS)

    print("Backup completed successfully.")
    return True

def cleanup_old_backups(backup_dir, retention_days):
    now = datetime.now()
    for filename in os.listdir(backup_dir):
        if filename.endswith(".tar.gz.enc"):
            file_path = os.path.join(backup_dir, filename)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mtime > timedelta(days=retention_days):
                os.remove(file_path)
                print(f"Removed old backup: {file_path}")

def main():
    if not create_backup():
        print("Backup failed.")

if __name__ == '__main__':
    main()
