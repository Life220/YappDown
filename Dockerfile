FROM alpine:latest

# Install necessary packages
RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    mariadb \
    mariadb-client \
    mariadb-dev \
    linux-headers \
    bash \
    py3-virtualenv \
    build-base

# Set up directory
RUN mkdir /YappDown
WORKDIR /YappDown

# Copy the existing Django project files
COPY YappDown /YappDown

# Create a virtual environment and activate it (PEP 668 compliance in Alpine Linux)
RUN python3 -m venv /YappDown/venv

# Upgrade pip and install Python packages within the virtual environment
RUN /YappDown/venv/bin/pip install --upgrade pip && \
    /YappDown/venv/bin/pip install django mysqlclient

# Expose port
EXPOSE 8000

# Set the hostname
RUN echo "127.0.0.1 localhost" > /etc/hosts

# Create and initialize the MariaDB data directory
RUN mkdir -p /var/lib/mysql && \
    chown -R mysql:mysql /var/lib/mysql && \
    mysql_install_db --user=mysql --datadir=/var/lib/mysql --force

# Copy the starter script and make it executable
COPY starter.sh starter.sh
RUN chmod +x starter.sh

# Use the starter script to start the services
CMD ["/bin/sh", "./starter.sh"]