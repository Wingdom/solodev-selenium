import boto3,json,os,subprocess,base64,time,shutil
from botocore.vendored import requests
import paramiko

import login

#Boot up tests
login = login.Login()

def lambda_handler(event, context):

    print("Run App")
    print(event)
    print(context)

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("At least one CloudFormation notification type needs to be specified")
        return

    # SNS topic ARN
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN", None)
    if not sns_topic_arn:
        print("The ARN of the SNS topic needs to be specified")
        return

    try:
        message = str(event["Records"][0]["Sns"]["Message"]).replace("\n", ",")
    except Exception:
        print("Message could not be parsed. Event: %s" % (event))
        return

    # Ignore resources that are not the CloudFormation stack itself
    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        return

    for notification_type in notification_types:
        if notification_type not in message:
            continue

        sns_subject = "CloudFormation %s" % (notification_type)
        sns_message = message.replace(",", "\n")

        if % (notification_type) == "CREATE_COMPLETE":
            dispatcher()


def dispatcher():
    login.test()
    return True