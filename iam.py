import boto3
from botocore.exceptions import ClientError

# Create a client
iam = boto3.client('iam')
# Create a group
group_name = "Managers"
try:
    response = iam.create_group(GroupName=group_name)

    print(f"IAM Group'{group_name}' created successfully.")
except ClientError as e:
    if e.response["Error"]['Code']=='EntityAlreadyExists':
        print(f"IAM Group '{group_name}' already exists.")
    else:
        print(f"Unexpected error: {e}")

# Attached a policy to the Group
policy_arn = "arn:aws:iam::242201265552:policy/s3"
try:
    iam.attach_group_policy(GroupName=group_name , PolicyArn=policy_arn)
    print(f"Policy'{policy_arn}' attached to group '{group_name}'")
except ClientError as e:
    print(f"Faild to attach policy: {e}")

# Create an User
user_name = "user_manager"
try:
    response = iam.create_user(UserName=user_name)
    print(f"IAM User '{user_name}' created successfully.")
except ClientError as e:
    if e.response['Error']['Code']=="EntityAlreadyExists":
        print(f"Iam User '{user_name}' already exists.")
    else:
        print(f"Unexpected error: {e}")

# Add user to a Group
try:
    iam.add_user_to_group(GroupName=group_name,UserName=user_name)
    print(f"User '{user_name}' added to group '{group_name}'.")
except ClientError as e:
    print(f"Failed to add user to group: {e}")