#rds mysql connect restore database



#!/bin/bash

# Install MySQL client
sudo apt-get update
sudo apt-get install -y mysql-client

# Connect to MySQL RDS instance
mysql -h endpoint -u admin -p

# Download SQL file from S3 bucket
aws s3 cp s3://ccldev-s3-upload/cprmse_bill_tracking.sql /tmp/

# Create a new database
CREATE DATABASE dbname;

# Create a new user and grant privileges
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dbname.* TO 'username'@'%';

# Flush privileges
FLUSH PRIVILEGES;

# Import data into the database from the SQL file
mysql -h endpoint -u username -p -D dbname < /tmp/cprmse_bill_tracking.sql

# Clean up: Remove the temporary SQL file
rm /tmp/cprmse_bill_tracking.sql
