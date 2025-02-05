#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status

# Prompt for required information
read -p "Enter the name of the zip file (without .zip extension): " PROJECT_NAME
read -p "Enter MySQL username for application: " MYSQL_USER
read -s -p "Enter MySQL password for application: " MYSQL_PASSWORD
echo

# Define variables
PROJECT_DIR="/root/$PROJECT_NAME"
ZIP_FILE="$PROJECT_NAME.zip"
DB_NAME="healthcheckdb"
WEBAPP_DIR="$PROJECT_DIR/"
ENV_FILE="$WEBAPP_DIR/.env"

# Function to set up swap memory
setup_swap() {
    echo "Setting up swap memory..."
    if ! sudo swapon --show | grep -q swapfile; then
        sudo fallocate -l 1G /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    else
        echo "Swap memory already configured."
    fi
}

echo "Starting setup..."

# 1. Configure swap before doing anything
setup_swap

# 2. Install dependencies
echo "Updating system and installing dependencies..."
sudo apt update 
sudo apt install -y unzip python3-pip python3-venv pkg-config libmysqlclient-dev mysql-server

# 3. Transfer and extract project files
echo "Extracting project files..."
cd /root/
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Zip file '$ZIP_FILE' not found!"
    exit 1
fi
unzip -o "$ZIP_FILE"

# 4. Navigate to the webapp folder
cd "$WEBAPP_DIR"

# 5. Setup virtual environment
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 6. Configure MySQL securely
echo "Configuring MySQL..."
sudo systemctl restart mysql

# Use debian-sys-maint credentials to configure MySQL
sudo mysql --defaults-file=/etc/mysql/debian.cnf <<EOF
-- Check and remove existing application user if needed
DROP USER IF EXISTS '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS ${DB_NAME};

-- Create dedicated application user
CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# Update .env file with application credentials
cat <<EOL > "$ENV_FILE"
DATABASE_USERNAME=${MYSQL_USER}
DATABASE_PASSWORD=${MYSQL_PASSWORD}
DATABASE_HOST=localhost
DATABASE_NAME=${DB_NAME}
DATABASE_PORT=3306
EOL

# 7. Install project dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 8. Initialize Flask DB
echo "Setting up Flask database..."
flask db init || echo "Flask DB already initialized."
flask db migrate -m "Initial migration" || echo "Migration step skipped (if already done)."
flask db upgrade

# 9. Run Flask application
echo "Starting Flask app..."
flask run --host=0.0.0.0 --port=5000

echo "Setup complete!"