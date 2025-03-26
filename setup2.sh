#!/bin/bash

# Exit on error
set -e

sudo groupadd -f csye6225
sudo useradd -r -g csye6225 -s /usr/sbin/nologin csye6225

sudo chown -R csye6225:csye6225 /var/log/webapp                  # Create log directory
sudo chmod -R 755 /var/log/webapp
sudo mkdir -p /opt/csye6225/webapp
sudo chown -R csye6225:csye6225 /opt/csye6225

sudo mv /tmp/csye6225.service /etc/systemd/system/
sudo mv /tmp/webapp.zip /opt/csye6225/webapp
sudo chown -R csye6225:csye6225 /opt/csye6225
sudo chmod -R 755 /opt/csye6225
cd /opt/csye6225/webapp
sudo unzip webapp.zip


sudo python3 -m venv venv
sudo bash -c "source venv/bin/activate && pip install -r requirements.txt"


sudo systemctl daemon-reload
sudo systemctl enable csye6225
sudo systemctl start csye6225



