# Dockerfile for the backup of the BICA database

# Base image
FROM postgres:13

LABEL name="Jodionisio Muachifi"
LABEL email="jodionisiomuachifi@ua.pt"

# Install dependencies (if needed)
RUN apt-get update && apt-get install -y cron

# Copy the backup script
COPY backup.sh /usr/local/bin/backup.sh

# Set execution permissions
RUN chmod +x /usr/local/bin/backup.sh

# Add crontab file in the cron directory
COPY cronfile /etc/cron.d/bica-backup

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/bica-backup

# Apply cron job
RUN crontab /etc/cron.d/bica-backup

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
