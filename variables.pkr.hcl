variable "AWS_REGION" {
  type    = string
  default = "AWS_REGION"
}

variable "SOURCE_AMI" {
  type    = string
  default = "ami-04b4f1a9cf54c11d0"
}

variable "SSH_USERNAME" {
  type    = string
  default = "ubuntu"
}


variable "DEV_USER" {
  type    = string
  default = "DEV_USER"
}

variable "DEMO_USER" {
  type    = string
  default = "DEMO_USER"
}

variable "AWS_ACCESS_KEY_ID" {
  type    = string
  default = "AWS_ACCESS_KEY_ID"
}

variable "AWS_SECRET_ACCESS_KEY" {
  type    = string
  default = "AWS_SECRET_ACCESS_KEY"
}

variable "MYSQL_ROOT_PASS" {
  type    = string
  default = "MYSQL_ROOT_PASS"
}

variable "MYSQL_ROOT_USER" {
  type    = string
  default = "MYSQL_ROOT_USER"
}

variable "DATABASE_USERNAME" {
  type    = string
  default = "DATABASE_USERNAME"
}

variable "DATABASE_PASSWORD" {
  type    = string
  default = "DATABASE_PASSWORD"
}

variable "DATABASE_HOST" {
  type    = string
  default = "DATABASE_HOST"
}

variable "DATABASE_NAME" {
  type    = string
  default = "DATABASE_NAME"
}

variable "INSTANCE_TYPE" {
  type    = string
  default = "t2.micro"
}

variable "project_id" {
  type    = string
  default = "devg"
}

variable "source_image" {
  type    = string
  default = "ubuntu"
}

variable "zone" {
  type    = string
  default = "us-east4-b"
}

variable "DISK_SIZE" {
  type    = string
  default = "10"
}

variable "machine_type" {
  type    = string
  default = "e2"
}