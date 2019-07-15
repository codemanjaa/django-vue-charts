FROM postgres:9.6

# Update the distribution and install dependencies from the official repos
RUN apt-get update && apt-get install -y cron rsyslog \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/locale/* && rm -rf /usr/share/man/* && rm -rf /usr/share/doc/*

RUN touch /etc/crontab
RUN touch /var/log/cron.log

COPY crontab /tmp/crontab
RUN crontab /tmp/crontab && rm /tmp/crontab

COPY backup.sh /usr/lib/jdfbots/backup.sh
RUN chmod +x /usr/lib/jdfbots/backup.sh

VOLUME /backups

ENTRYPOINT rsyslogd && cron && tail -f /var/log/cron.log /var/log/syslog