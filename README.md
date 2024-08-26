BICA PostgreSQL Backup Solution
Overview

This repository provides a solution to automate the backup of a PostgreSQL database using Docker. The solution is designed to run within a Docker container and is scheduled to perform backups twice daily. The backup files are stored locally with a retention policy, and the process is robust enough to resume after server restarts.
Features

    Automated backups twice a day (03:00 AM and 14:00 PM UTC).
    Backup files are named with a timestamp and compressed for efficient storage.
    Backup retention policy to automatically delete old backups.
    Supports environment variables for easy customization of database connection details.
    Containerized with Docker for easy deployment and portability.
    Optionally, backups can be encrypted.

Requirements

    Docker and Docker Compose installed on the server.
    A PostgreSQL database that the backup script can connect to.
    Sufficient storage in the /mnt/backups directory.

Files in the Repository

    backup.sh: The main script that performs the backup, compresses it, and manages retention.
    Dockerfile: Defines the Docker image that will run the backup script.
    cronfile: Specifies the schedule for running the backup script.
    docker-compose.yml: Configuration file for deploying the backup solution using Docker Compose.
    .env: Optional file for defining environment variables.

Setup Instructions
1. Clone the Repository

bash

git clone <repository-url>
cd <repository-directory>

2. Configure Environment Variables

Create a .env file in the root of the repository to define the necessary environment variables:

bash

DB_HOST=your_db_host
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name
RETENTION_DAYS=7

    DB_HOST: The hostname or IP address of the PostgreSQL server.
    DB_PORT: The port number for the PostgreSQL server (default is 5432).
    DB_USER: The username for accessing the PostgreSQL database.
    DB_PASS: The password for the PostgreSQL user.
    DB_NAME: The name of the database to back up.
    RETENTION_DAYS: Number of days to keep the backup files before they are deleted.

3. Build and Deploy the Docker Container

Use Docker Compose to build the Docker image and deploy the container:

bash

docker-compose up -d

    The -d flag runs the container in detached mode.

4. Verify Backup Creation

You can manually trigger the backup script inside the container for testing:

bash

docker exec -it bica-backup /usr/local/bin/backup.sh

Check the /mnt/backups directory to ensure that the backup files are being created and stored properly.
5. Monitoring and Logs

Logs for the backup process are stored within the container and can be accessed with:

bash

docker logs bica-backup

To monitor the crontab jobs and ensure they are running correctly:

bash

docker exec -it bica-backup tail -f /var/log/cron.log

6. Stop the Backup Service

To stop the container and backup service:

bash

docker-compose down

This will stop and remove the container without deleting the backup files.
Customizations
Adjusting the Backup Schedule

The backup schedule is controlled by the cronfile. To change the schedule, modify the cron expression in cronfile:

bash

# Current Schedule: 03:00 AM and 14:00 PM UTC
0 3,14 * * * /usr/local/bin/backup.sh >> /var/log/cron.log 2>&1

Enabling Backup Encryption

To enable encryption for your backups, uncomment the relevant lines in backup.sh and set an encryption password:

bash

# Uncomment and set your encryption password
# ENCRYPTION_PASSWORD="your_encryption_password"
# openssl enc -aes-256-cbc -salt -in $BACKUP_FILE -out ${BACKUP_FILE}.enc -k $ENCRYPTION_PASSWORD
# mv ${BACKUP_FILE}.enc $BACKUP_FILE

Adjusting Retention Policy

You can modify the RETENTION_DAYS variable in your .env file to change how long backups are kept before deletion.
Troubleshooting
Backup Files Not Appearing

    Ensure that the database connection details in .env are correct.
    Check the permissions of the /mnt/backups directory to ensure the container can write to it.

Cron Jobs Not Running

    Verify that the cronfile is correctly configured and applied by checking the cron logs:

bash

docker exec -it bica-backup tail -f /var/log/cron.log

Container Not Restarting After Failure

    Ensure that the restart: always policy is set in docker-compose.yml.

Conclusion

This Docker-based solution provides a robust and flexible way to automate PostgreSQL backups. By following the instructions above, you can easily deploy this solution on your server and ensure that your database backups are handled automatically and securely.
