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
- `.env`: (Optional) Environment variable definitions

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Configure environment variables in a .env file:
   ```DB_HOST=your_db_host
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name
RETENTION_DAYS=7
```
