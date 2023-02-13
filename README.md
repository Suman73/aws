# aws
Multiple small project i created all are listed according to service 





project cloud watch to sns

import json
import boto3



def lambda_handler(event, context):
    
        sns_client = boto3.client("sns")
        
        obs=1
        
        if obs:
            print("Oh nice this is working")
            sns_client.publish(TopicArn="arn:aws:sns:ap-south-1:344542533384:mytopic", Message="Hi suman How are ", Subject="HISuman")
        else:
            print("There is some issue")
