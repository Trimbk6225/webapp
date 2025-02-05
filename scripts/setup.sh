#!/bin/bash

set -e # Stop execution immediately if any command fail

# Collect user input
read -p "Provide the zip file name without extension: " PROJECT_NAME
echo

# Define variables
APP_GROUP="myappgroup"  # Linux group assigned for the application
ZIP_FILE="$PROJECT_NAME.zip"
DB_NAME="healthcheckdb"  # Updated as per config.py
APP_USER="myappuser"  # Linux user assigned for application
APP_DIR="/opt/csye6225"  # Directory where the application will be deployed

echo "Initiating setup process..."

# 2. Install necessary dependencies
echo "Updating system and installing dependencies..."
sudo apt update && sudo apt install -y unzip python3-pip python3-venv pkg-config mysql-server

# 3. Configure MySQL database and user
echo "Setting up MySQL database and user account..."
sudo systemctl restart mysql

read -p "Specify the MySQL username: " MYSQL_USER
read -s -p "Enter the MySQL password: " MYSQL_PASSWORD
echo 

# Secure MySQL setup and grant permissions
sudo mysql --defaults-file=/etc/mysql/debian.cnf <<EOF
DROP USER IF EXISTS '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# 4. Establish Linux user and group for the application
echo "Creating system user and group for application management..."
sudo groupadd -f "$APP_GROUP"
if id "$APP_USER" &>/dev/null; then
    echo "User $APP_USER is already present"
else
    sudo useradd -g "$APP_GROUP" -m -d "$APP_DIR" "$APP_USER"
fi

# 5. Extract application files
echo "Unzipping project files into $APP_DIR..."
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: File '$ZIP_FILE' is missing!"
    exit 1
fi
sudo unzip -o "$ZIP_FILE" -d "$APP_DIR"

# 6. Adjust permissions for application directory
sudo chown -R $APP_USER:$APP_GROUP $APP_DIR
sudo chmod -R 755 $APP_DIR

# 7. Move into application folder
WEBAPP_DIR="$APP_DIR/$PROJECT_NAME/webapp"
cd "$WEBAPP_DIR"

# 8. Set up Python virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 9. Configure environment settings dynamically
echo "Updating .env file with database credentials..."
cat <<EOL > ".env"
DATABASE_USERNAME=$MYSQL_USER
DATABASE_PASSWORD=$MYSQL_PASSWORD
DATABASE_HOST=localhost
DATABASE_NAME=$DB_NAME
DATABASE_PORT=3306
EOL

# 10. Install required Python libraries
pip install --upgrade pip
pip install -r requirements.txt

# 11. Set up the database for Flask
flask db init || echo "done"
flask db migrate -m "Initial setup migration" || echo "done"
flask db upgrade

# 12. Launch Flask application
sudo -u $APP_USER bash -c "source $WEBAPP_DIR/venv/bin/activate && flask run --host=0.0.0.0 --port=5000"
