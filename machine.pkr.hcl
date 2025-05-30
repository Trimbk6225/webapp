packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0, <2.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}
packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
  }
}



source "amazon-ebs" "my_ami" {
  ami_name        = "csye6225_f25_app_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  instance_type   = var.INSTANCE_TYPE
  region          = var.AWS_REGION
  ami_description = "AMI FOR CSYE 6225"

  source_ami   = var.SOURCE_AMI
  ssh_username = var.SSH_USERNAME
  ami_users    = [var.DEV_USER, var.DEMO_USER]

  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
    delete_on_termination = true
  }
}

#gcp
source "googlecompute" "gcp_ami" {
  image_name        = "gcp6225f25app${formatdate("YYYYMMDD", timestamp())}"
  image_description = "image on gcp"
  project_id        = "${var.project_id}"
  source_image      = "${var.source_image}"
  ssh_username      = "${var.SSH_USERNAME}"
  zone              = "${var.zone}"
  disk_size         = var.disk_size
  machine_type      = "${var.machine_type}"
}

# Build configuration

build {
  name = "A4"
  sources = [
    "source.amazon-ebs.my_ami",
    # "source.googlecompute.gcp_ami",
  ]
  provisioner "file" {
    source      = "./cloudwatch-config.json"   
    destination = "/tmp/cloudwatch-config.json"
  }
  # Create /var/log/webapp directory and configure CloudWatch Agent
  provisioner "shell" {
    inline = [
      "sudo mkdir -p /var/log/webapp",
      # "sudo chown -R csye6225:csye6225 /var/log/webapp",                  
      # "sudo chmod -R 755 /var/log/webapp",                
      "sudo apt-get update",
      "sudo apt-get install -y wget",
      "wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb", 
      "sudo dpkg -i amazon-cloudwatch-agent.deb",                                                            
      # "rm amazon-cloudwatch-agent.deb",                  
      # "sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc/", # Ensure config directory exists
      #  "[[ -f /tmp/cloudwatch-config.json ]] && sudo mv /tmp/cloudwatch-config.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json || echo 'Config file not found!'" ,# Move config file
      "sudo mv /tmp/cloudwatch-config.json /opt/",
      "sudo systemctl enable amazon-cloudwatch-agent", 
      "sudo systemctl start amazon-cloudwatch-agent",  
    ]
  }

  # Copy the CloudWatch configuration file to the instance



  # provisioner "file" {
  #   source      = "./.env"
  #   destination = "/tmp/"
  # }

  provisioner "file" {
    source      = "csye6225.service"
    destination = "/tmp/"
  }

  # Provision application files
  provisioner "file" {
    source      = "webapp.zip"
    destination = "/tmp/"
  }

  provisioner "shell" {

    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1",
      # "DATABASE_USERNAME=${var.DATABASE_USERNAME}",
      # "DATABASE_PASSWORD=${var.DATABASE_PASSWORD}",
      # "DATABASE_HOST=${var.DATABASE_HOST}",
      # "DATABASE_NAME=${var.DATABASE_NAME}",
      # "MYSQL_ROOT_USER=${var.MYSQL_ROOT_USER}",
      # "MYSQL_ROOT_PASS=${var.MYSQL_ROOT_PASS}",
    ]


    inline = [
      # "export MYSQL_ROOT_USER=${var.MYSQL_ROOT_USER}",
      # "export MYSQL_ROOT_PASS=${var.MYSQL_ROOT_PASS}",
      # "export DATABASE_USERNAME=${var.DATABASE_USERNAME}",
      # "export DATABASE_PASSWORD=${var.DATABASE_PASSWORD}",
      # "export DATABASE_HOST=${var.DATABASE_HOST}",
      # "export DATABASE_NAME=${var.DATABASE_NAME}",

      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt install -y unzip",
      "sudo apt install -y python3-pip",
      "sudo apt install -y python3-venv",
      "sudo apt install -y pkg-config",
      # "sudo apt install -y mysql-server",
      "sudo apt remove --purge git -y",
      "sudo apt autoremove -y",
      # "sudo systemctl enable mysql",
      # "sudo systemctl start mysql",


      # Proceed with MySQL commands after setting the root password
      # "sudo mysql -u root -proot -e \"CREATE USER '$DATABASE_USERNAME'@'$DATABASE_HOST' IDENTIFIED BY '$DATABASE_PASSWORD'; CREATE DATABASE $DATABASE_NAME; GRANT ALL PRIVILEGES ON $DATABASE_NAME.* TO '$DATABASE_USERNAME'@'$DATABASE_HOST' WITH GRANT OPTION; FLUSH PRIVILEGES;\""
    ]
  }


  provisioner "shell" {
    script = "setup2.sh"
  }

  post-processor "manifest" {
    output = "manifest.json"
  }


}


