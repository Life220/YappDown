FROM alpine:latest

# Set the timezone to UTC+2
ENV TZ=Etc/GMT-2

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
    icu-data-full \
    bash \
    py3-virtualenv \
    build-base \
    tzdata \
    nodejs \
    npm

# Set up directory
RUN mkdir /YappDown
WORKDIR /YappDown
COPY YappDown /YappDown

# Create a virtual environment and activate it (PEP 668 compliance in Alpine Linux)
RUN python3 -m venv /YappDown/venv

# Upgrade pip and install Python packages within the virtual environment
RUN /YappDown/venv/bin/pip install --upgrade pip && \
    /YappDown/venv/bin/pip install django mysqlclient && \
    /YappDown/venv/bin/pip install psutil

## Tailwind CSS
# Copy package.json
COPY package.json /YappDown/

# Install Tailwind CSS
RUN npm install tailwindcss

# Initialize Tailwind CSS
RUN npx tailwindcss init
RUN echo "module.exports = { plugins: [require('tailwindcss'), require('autoprefixer')], };" > postcss.config.js

# Copy the Tailwind CSS input file
COPY YappDown/app/static/tailwind.css /YappDown/app/static/tailwind.css

# Build Tailwind CSS
RUN npm run build:css

# Expose port
EXPOSE 8000

# Create and initialize the MariaDB data directory
RUN mkdir -p /var/lib/mysql && \
    chown -R mysql:mysql /var/lib/mysql && \
    mysql_install_db --user=mysql --datadir=/var/lib/mysql --force

# Copy the starter script and make it executable
COPY starter.sh starter.sh
RUN chmod +x starter.sh

# Use the starter script to start the services
CMD ["/bin/sh", "./starter.sh"]