import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Specify your EC2 instance ID and region here
    instance_id = '#put your instance id'
    region = 'ap-south-1'

    # Connect to EC2
    ec2 = boto3.client('ec2', region_name=region)

    # Create a timestamp for the AMI name
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    # Create an AMI
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=f'AMI-{timestamp}',
        Description=f'AMI created at {timestamp}',
        NoReboot=True
    )

    # Add a tag to the created AMI with the instance ID
    ami_id = response['ImageId']
    ec2.create_tags(Resources=[ami_id], Tags=[{'Key': 'InstanceId', 'Value': instance_id}])

    print(f'AMI {ami_id} created successfully with name AMI-{timestamp} and tagged with InstanceId: {instance_id}')

    # List all AMIs and filter by tag
    amis = ec2.describe_images(
        Owners=['self'],
        Filters=[
            {'Name': 'tag:InstanceId', 'Values': [instance_id]}
        ]
    )['Images']
    
    print("List all AMIs and filter by tag", amis)
    
    # Filter AMIs older than 48 hours
    amis_to_delete = []
    current_time = datetime.utcnow()

    for ami in amis:
        ami_creation_time = datetime.strptime(ami['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ami_age = current_time - ami_creation_time

        if ami_age > timedelta(minutes=5):
            amis_to_delete.append(ami)
            print(f'AMI {ami["ImageId"]} created at {ami_creation_time} is older than 48 hours.')

    # Now, amis_to_delete contains the list of AMIs older than 48 hours
    print("AMIs to delete:", amis_to_delete)

    # Deregister and delete snapshots for all AMIs in amis_to_delete
    for ami in amis_to_delete:
        # Deregister AMI
        ec2.deregister_image(ImageId=ami['ImageId'])
        print(f'Deregistered AMI {ami["ImageId"]}')

        # Delete associated snapshots
        for block_device in ami['BlockDeviceMappings']:
            snapshot_id = block_device.get('Ebs', {}).get('SnapshotId')
            if snapshot_id:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f'Deleted Snapshot {snapshot_id}')

    return {
        'statusCode': 200,
        'body': f'AMI cleanup completed successfully'
    }

#Inline IAM Json Policy
"""
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateImage",
                "ec2:CreateTags",
                "ec2:DescribeImages",
                "ec2:DeregisterImage",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        }
    ]
}
"""






