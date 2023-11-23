import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    # Set your AWS region
    aws_region = 'ap-south-1'

    # Set the date before which snapshots should be deleted
    delete_before_date = datetime(2023, 11, 22, tzinfo=timezone.utc)

    # Create an EC2 client
    ec2_client = boto3.client('ec2', region_name=aws_region)

    # Describe snapshots that match your criteria
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']

    # Filter snapshots created before the specified date
    snapshots_to_delete = [snapshot['SnapshotId'] for snapshot in snapshots if snapshot['StartTime'] > delete_before_date]
    
    print(snapshots_to_delete)
    
    
    

    return {
        'statusCode': 200,
        'body': f'Deleted {len(snapshots_to_delete)} snapshots created before {delete_before_date}.'
    }
