FROM python:3.6
LABEL maintainer "Fabien Dubosson <fabien.dubosson@gmail.com>"

# Update the distribution and install dependencies from the official repos
RUN apt-get update && apt-get install -y nginx supervisor \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/locale/* && rm -rf /usr/share/man/* && rm -rf /usr/share/doc/*

# Install dependencies from pip
RUN pip install uwsgi

# Configure nginx
COPY containers/server/nginx.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/sites-enabled/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Configure supervisor
COPY containers/server/supervisord.conf /etc/supervisor/conf.d/

# Configure uwsgi
RUN mkdir /etc/uwsgi/
COPY containers/server/uwsgi.ini /etc/uwsgi/uwsgi.ini

# Prepare the app at build time
RUN mkdir -p /var/jdf /var/jdf/logs
COPY ./ /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Remove unneeded files
RUN cd /app

# Fix permissions
RUN chown www-data:www-data -R /app /var/jdf

# Declare container parameters
WORKDIR /app
VOLUME [ "/var/jdf" ]
EXPOSE 80

# Define command to run
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
