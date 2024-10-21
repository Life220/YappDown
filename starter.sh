# Ensure proper permissions for MariaDB
echo "Setting permissions for MariaDB..."
chown -R mysql:mysql /var/lib/mysql

# Start MariaDB service
echo "Starting MariaDB..."
/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &

# Wait for MariaDB to start
echo "Waiting for MariaDB to start..."
while ! mysqladmin ping --silent; do
    sleep 1
done

# Check if MariaDB started successfully
if ! mysqladmin ping --silent; then
    echo "MariaDB failed to start."
    exit 1
fi

# Create the database and user if they do not exist
echo "Setting up the database..."
mysql -e "CREATE DATABASE IF NOT EXISTS YappDownDB;"
mysql -e "CREATE USER 'Yapper'@'localhost' IDENTIFIED BY 'TimeToYap';"
mysql -e "GRANT ALL PRIVILEGES ON YappDownDB.* TO 'Yapper'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# Apply database migrations
echo "Applying database migrations..."
/YappDown/venv/bin/python3 /YappDown/manage.py makemigrations
/YappDown/venv/bin/python3 /YappDown/manage.py migrate

# Start the Django development server
echo "Starting Django development server..."
/YappDown/venv/bin/python3 /YappDown/manage.py runserver 0.0.0.0:8000