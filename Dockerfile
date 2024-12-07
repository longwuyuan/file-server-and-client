# Use nginx as base image instead of python to take advantage of the default nginx configuration
FROM nginx:alpine

# To reduce image layers, all custom files are under /app so that there is only one layer for Dockerfile COPY
COPY app /app

# NOTES on exception of running python app without virtualenv
# - Supervisord is being used to launch both nginx & gunicorn
# - Supervisord runs as root because it launches nginx daemon, that needs to bind to low port 80 (and potentially 443)
# - Nginx frontend in the docker image provides standards based reverseproxy config for upstream flask-app
# - Gunicorn backend in the same docker image provides production grade uWSGI server to run the flask-app
# - For security, its better to run process as non-root. But for support/maintenance, a root shell is needed.
# - Hence running app processes as root, is a acceptable exception to aid support/maintenance & observability integrations
# - Servicemessh & eBPF require root

# Install supervisor, python, gunicorn & flask-app dependencies 
RUN apk upgrade && apk add git supervisor python3 py3-pip --no-cache && \
  pip install --no-cache-dir -r /app/requirements.txt  --break-system-packages && \
  # Place the app & config files in required paths 
  # Configure the container
  mv /app/conf/nginx.vhost.conf /etc/nginx/conf.d/default.conf && \
  mv /app/conf/supervisord.conf /etc/supervisord.conf && \
  rm -rf /app/conf && \
  # Assist supervisor configuration
  mkdir /etc/supervisor.d /var/log/supervisord 

WORKDIR /app

EXPOSE 80

CMD ["/usr/bin/supervisord"]
