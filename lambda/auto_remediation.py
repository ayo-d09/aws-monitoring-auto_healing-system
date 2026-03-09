import json
import boto3

ec2 = boto3.client("ec2")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        # Parse SNS message from CloudWatch Alarm
        message = json.loads(event['Records'][0]['Sns']['Message'])

        # Get instance ID from alarm dimensions
        instance_id = message['Trigger']['Dimensions'][0]['value']

        print(f"Rebooting EC2 instance: {instance_id}")

        # Reboot the EC2 instance
        ec2.reboot_instances(InstanceIds=[instance_id])

        return {
            "statusCode": 200,
            "body": f"Instance {instance_id} reboot initiated"
        }

    except Exception as e:
        print("Error:", str(e))
        raise