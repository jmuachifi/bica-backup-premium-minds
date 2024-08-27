# backup.sh: Backup script for PostgreSQL databases.

#!/bin/bash

# Variables
# export $(grep -v '^#' .env | xargs)

# Use the environment variables if necessary
# DB_HOST=${DB_HOST}
# DB_PORT=${DB_PORT}
# DB_USER=${DB_USER}
# DB_PASS=${DB_PASS}
# DB_NAME=${DB_NAME}
# BACKUP_DIR=${BACKUP_DIR:-"/mnt/backups"}
# RETENTION_DAYS=${RETENTION_DAYS:-7}
# ENCRYPTION_PASSWORD=${ENCRYPTION_PASSWORD}

DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-"postgres"}
DB_PASS=${DB_PASS:-"password"}
DB_NAME=${DB_NAME:-"postgres"}
BACKUP_DIR=${BACKUP_DIR:-"/mnt/backups"}
RETENTION_DAYS=${RETENTION_DAYS:-7}
ENCRYPTION_PASSWORD=${ENCRYPTION_PASSWORD:-"passwordencryption"}

# Timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")

# Backup file name
BACKUP_FILE="${BACKUP_DIR}/bica-backup-${TIMESTAMP}.tar.gz"

# Export the password for pg_dump
export PGPASSWORD=$DB_PASS

# Create a backup
echo "Creating backup..."
if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME | gzip > $BACKUP_FILE; then
  echo "Backup created: $BACKUP_FILE"
else
  echo "Error: pg_dump failed."
  unset PGPASSWORD
  exit 1
fi

# Encrypt the backup file
ENCRYPTED_FILE="${BACKUP_FILE}.enc"
echo "Encrypting backup..."
if openssl enc -aes-256-cbc -pbkdf2 -salt -in $BACKUP_FILE -out $ENCRYPTED_FILE -k $ENCRYPTION_PASSWORD; then
  echo "Encryption successful: $ENCRYPTED_FILE"
else
  echo "Error: Encryption failed."
  rm $BACKUP_FILE
  unset PGPASSWORD
  exit 1
fi

# Remove the unencrypted backup file
rm $BACKUP_FILE

# Remove backups older than retention days
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -name "*.tar.gz" -exec rm {} \;

# Unset the password
unset PGPASSWORD

echo "Backup completed successfully."
