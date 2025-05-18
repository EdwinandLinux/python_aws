import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

# Create VPC
vpc = ec2_resource.create_vpc(CidirBlock='10.0.0.0/16')
vpc.wait_until_available()
vpc.create_tags(Tags=[{'Key':'Name' , 'Value':'MyVPC'}])
vpc.modify_attribute(EnableDnsSupport={'Value':True})
vpc.modify_attribute(EnableDNSHostnames={'Value':True})
vpc_id = vpc.id
print(vpc_id)

# Attached Internate gateway to the VPC
igw  =ec2_resource.create_internet_gateway()
igw.attach_internet_gateway(InternetGatewayId=igw.id)

# Create Subnets
public_subnet = ec2_resource.create_subnet(VpcId=vpc.id , CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
private_subnet = ec2_resource.create_subnet(VpcId=vpc.id , CidrBlock='10.0.2.0/24' , AvailabilityZone= 'us-east-1a')

# Create Route Tables and Routes
public_route_table = ec2_resource.create_route_table(VpcId=vpc.id)
public_route_table.create_route(DestinationCidrBlock='0.0.0.0/0' , GatewayId=igw.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet.id)

private_route_table = ec2_resource.create_route_table(VpcId=vpc.id)
private_route_table.associate_with_subnet(SubnetId=private_subnet.id)

# Create Security Group
security_group = ec2_resource.create_security_group(GroupName="my-sg",Description='Allow SSH and HHTP',VpcId=vpc.id)
security_group.authorize_ingress(
    IpPermissions =[{
        'IpProtocol':'tcp', 'FromPort':22, 'ToPort':22 , 'IpRanges': [{'CidrIp':'0.0.0.0/0'}]},
        {'IpProtocol':'tcp', 'FromPort':80, 'ToPort':80 , 'IpRanges': [{'CidrIp':'0.0.0.0/0'}]},
    ]
)

# Create Network ACL
nacl = ec2_resource.create_network_acl(VpcId = vpc.id)
# TThis creates an inbound (Egress=False) rule. It allows all traffic (Protocol='-1', which means any protocol) from the entire internet (CidrBlock='0.0.0.0/0'). The rule has a number of 100
nacl.create_entry(CidrBlock='0.0.0.0/0' , RuleNumber=100 , Protocol='-1' , RuleAction='allow' , Egress=False )
# This creates an outbound (Egress=True) rule. It allows all traffic (Protocol='-1') to the entire internet (CidrBlock='0.0.0.0/0'). The rule also has a number of 100
nacl.create_entry(CidrBlock='0.0.0.0/0' , RuleNumber=100 , Protocol='-1' , RuleAction='allow' , Egress=True )

# Associate NACLS with Subnets
ec2_client.associate_network_acl(SubnetId = public_subnet.id, NetworkAclId=nacl.id)
ec2_client.associate_network_acl(SubnetId = private_subnet.id, NetworkAclId=nacl.id)

# Launch EC2 Instances
ami_id = ""
key_name=""
# Public Instance
public_instance = ec2_resource.create_instance(
    ImageId = ami_id,
    InstanceType='t2.micro',
    MaxCount=1 ,
    MinCount =1 ,
    KeyName=key_name,
    NetworkInterfaces=[{
        'SubnetId':public_subnet.id,
        'DeviceIndex':0,
        'AssociatePublicIpAddress':True,
        'Groups':[security_group.id]

    }]
)[0]

# Private Instance
private_instance = ec2_resource.create_instance(
    ImageId = ami_id,
    InstanceType='t2.micro',
    MaxCount=1 ,
    MinCount =1 ,
    KeyName=key_name,
    NetworkInterfaces=[{
        'SubnetId':private_subnet.id,
        'DeviceIndex':0,
        'AssociatePublicIpAddress':False,
        'Groups':[security_group.id]

    }]
)[0]

print("VPC and infrastructure created successfully.")
print(f"Public instance ID {public_instance.id}")
print(f"Private instance ID {private_instance.id}")

# To test:

# SSH into the public instance: ssh -i <your-key.pem> ec2-user@<public-ip>

# From the public instance, test connectivity to the private one using its private IP