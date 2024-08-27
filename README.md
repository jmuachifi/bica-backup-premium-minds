# BICA PostgreSQL Backup Solution

## Overview

This repository provides an automated solution for backing up PostgreSQL databases using Docker. It's designed to run within a Docker container and perform backups twice daily. The backup files are stored locally with a configurable retention policy, and the process is resilient enough to resume after server restarts.

## Features

- Automated backups twice a day (03:00 AM and 14:00 PM UTC)
- Backup files are timestamped and compressed for efficient storage
- Configurable backup retention policy
- Supports environment variables for easy customization of database connection details
- Containerized with Docker for easy deployment and portability
- Optional backup encryption

## Requirements

- Docker and Docker Compose installed on the server
- A PostgreSQL database accessible to the backup script
- Sufficient storage in the `/mnt/backups` directory

## Repository Contents

- `backup.sh`: Main backup script
- `Dockerfile`: Defines the Docker image
- `cronfile`: Specifies the backup schedule
- `docker-compose.yml`: Configuration for Docker Compose deployment
- `.env`: (Optional) Environment variable definitions. This vars will be here just for test, but in production I could not show/send on github or expose anywhere.
- `py-version`: (optional) a folder with Python version for this exercice.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Configure environment variables in a .env file:
   ```
   DB_HOST=your_db_host
   DB_PORT=5432
   DB_USER=your_db_user
   DB_PASS=your_db_password
   DB_NAME=your_db_name
   RETENTION_DAYS=7
   ```
3. Build and deploy the Docker container:
   ```
    docker-compose up -d
    ```
4. Verify backup creation:
   ```
      docker exec -it bica-backup /usr/local/bin/backup.sh
   ```
> After running the script, check the BACKUP_DIR (e.g., /mnt/backups) to verify that a new backup file has been created. The file should be named something like bica-backup-YYYY-MM-DD_HHMM.tar.gz, where YYYY-MM-DD_HHMM is the timestamp
5. Monitor logs:
   ```
      docker logs bica-backup
   ```
6. List all backup inside a container:
   ```
      docker exec -it <container_name_or_id> ls -la /mnt/backups
   ```
7. Stop the backup service:
   ```
      docker-compose down
   ```
8. If you want to decrypt the backup, use this cmd: <br>
      ```
            sudo openssl enc -aes-256-cbc -d -pbkdf2 -salt -in /mnt/backups/bica-backup-2024-08-27_1428.tar.gz.enc -out /mnt/backups/bica-backup-2024-08-27_1428_decrypted.tar.gz -k "passwordencryption"
   ```
 > Please, change *bica-backup-2024-08-27_1428.tar.gz.enc* with your backup file with specific data time <br>

## If you want to test the backup locally (Manually)
   ```
   # First make sure you Postgress server installed or you can install as follows:
   sudo apt-get update
   sudo apt-get install postgresql && apt install postgresql-client

   # Load environment variables from .env file
   source .env

   # Run the backup script
   ./backup.sh

   # Check the backup directory to see if the new backup file is created
   ls -l /mnt/backups
   ```

## Customizations

- Adjust backup schedule by modifying cronfile
- Enable backup encryption by uncommenting relevant lines in backup.sh
- Modify retention policy by changing RETENTION_DAYS in .env

## Troubleshooting

- Ensure correct database connection details in .env
- Check permissions of /mnt/backups directory
- Verify cron job configuration in cronfile
- Ensure restart: always policy is set in docker-compose.yml
   
