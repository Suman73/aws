
import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    # Set your AWS region
    aws_region = 'ap-south-1'

    # Set the date after which AMIs should be deregistered
    deregister_after_date = datetime(2023, 11, 22, tzinfo=timezone.utc)

    # Create an EC2 client
    ec2_client = boto3.client('ec2', region_name=aws_region)

    # Describe AMIs that match your criteria
    images = ec2_client.describe_images(Owners=['self'])['Images']

    # Extract AMI IDs created after the specified date
    ami_ids_to_deregister = [
        image['ImageId'] 
        for image in images 
        if datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc) > deregister_after_date
    ]

    # Print the list of AMI IDs to be deregistered
    print("AMIs to be deregistered:", ami_ids_to_deregister)

    # Deregister AMIs
    for ami_id in ami_ids_to_deregister:
        ec2_client.deregister_image(ImageId=ami_id)

    return {
        'statusCode': 200,
        'body': f'Deregistered {len(ami_ids_to_deregister)} AMIs created after {deregister_after_date}.'
    }
