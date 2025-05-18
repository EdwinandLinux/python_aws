import boto3
import time

# Initialize EC2 Client
ec2 = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.resource('ec2')

# Create VPC and Public Subnet
vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16", TagSpecifications=[
        {
             'ResourceType': 'vpc',
            'Tags': [

                {
                    'Key': 'Mame',
                    'Value': 'Mvpc'
                },
            ]
        },
    ],)

vpc_id = vpc["Vpc"]['VpcId']
print(f"Create VPV {vpc_id}")
#vpc_id = "vpc-0bb68ae14dc804ef7"

# Enable DNS Support and Hostname
ec2.modify_vpc_attribute(VpcId=vpc_id , EnableDnsSupport={'Value':True})
ec2.modify_vpc_attribute(VpcId=vpc_id ,EnableDnsHostnames={'Value':True})

public_subnet = ec2.create_subnet(VpcId=vpc_id , CidrBlock='10.0.1.0/24', TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {'Key': 'Name', 'Value': 'Public Subnet'}
            ]
        }
    ])
public_subnet_id = public_subnet['Subnet']['SubnetId']

# Modify Subnet to auto-assign Public IPs
ec2.modify_subnet_attribute(SubnetId = public_subnet_id , MapPublicIpOnLaunch ={"Value":True})
print(f"Created Public Subnet {public_subnet_id}")

# Create a attach Internet Gateway
igw = ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=igw_id , VpcId = vpc_id)
print(f"Created and attached Internet Gateway {igw_id}")

# Create Route Table and Route
rt = ec2.create_route_table(VpcId = vpc_id)
rt_id  = rt['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId = rt_id , DestinationCidrBlock= '0.0.0.0/0' , GatewayId = igw_id)
ec2.associate_route_table(RouteTableId = rt_id , SubnetId = public_subnet_id)
print(f"Created and associated Route Table {rt_id}")

# Create Security Group for SSH and HTTP
sg  = ec2.create_security_group(GroupName = "sg" , Description="Allow SSH and HTTP" , VpcId = vpc_id)
sg_id =sg['GroupId']
ec2.authorize_security__group_ingress(
    GroupId = sg_id,
    IpPermissions=[
        {'IpProtocol':'tcp', 'FromPort':22 , 'ToPort':22,
        'IpRanges':[{'CidrIp':'0.0.0.0/0'}],
'IpProtocol':'tcp', 'FromPort':80 , 'ToPort':80,
        'IpRanges':[{'CidrIp':'0.0.0.0/0'}],

        }
    ]
)

# Launch EC2 instance
ami_id ="YOUR_AMI"
key_name="YOUR_KEY"
user_data_script = '''#!/bin/bash
sudo yum update -y
sudo yum install http -y
sudo systemctl start httpd
sudo systemctl enable httpd --now
echo "<h1>Hello EC2 instance</h1> >/var/www/html/index.html
'''
ec2_instance = ec2.run_instance(
    ImageId = ami_id ,
    InstanceType = 't2.micro',
    KeyNmae = key_name,
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId':public_subnet_id,
        'DeviceIndex':0,
        'AssociatePublicIpAddress':True,
        'Groups':[sg_id],

    }],
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType':'instance',
            'Tags':[
                {
                    'Key':'Name',
                    'Value':'WebServer'
                }
            ]
        }
    ]


)
instance_id = ec2_instance['Instances'][0]['InstanceId']
print(f"Launched EC2 instance: {instance_id}")