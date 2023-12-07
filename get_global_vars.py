#!/usr/bin/env python3

import os
import boto3

#AWS region
region = "eu-central-1"  
instance_id = os.popen("curl -s http://169.254.169.254/latest/meta-data/instance-id").read().strip()

ec2 = boto3.client("ec2", region_name=region)
response = ec2.describe_instances(InstanceIds=[instance_id])

if "Reservations" in response and len(response["Reservations"]) > 0:
    instance = response["Reservations"][0]["Instances"][0]
    instance_name = instance.get("Tags", [{}])[0].get("Value", "N/A")
    instance_id = instance["InstanceId"]
    account_number = boto3.client("sts").get_caller_identity().get("Account")
else:
    instance_name = "N/A"
    instance_id = "N/A"
    account_number = "N/A"

public_ip = os.popen("curl -s http://169.254.169.254/latest/meta-data/public-ipv4").read().strip()
private_ip = os.popen("curl -s http://169.254.169.254/latest/meta-data/local-ipv4").read().strip()

# Global variables in /opt/output.txt
with open("/opt/output.txt", "w") as output_file:
    output_file.write(f"Value of variable: variable name\n")
    output_file.write(f"region name: {region}\n")
    output_file.write(f"AZ name: {instance['Placement']['AvailabilityZone']}\n")
    output_file.write(f"public IP address: {public_ip}\n")
    output_file.write(f"private IP address: {private_ip}\n")
    output_file.write(f"name of instance: {instance_name}\n")
    output_file.write(f"instance ID: {instance_id}\n")
    output_file.write(f"account number: {account_number}\n")
