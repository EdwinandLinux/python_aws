import time
import boto3

# Create VPC
def create_vpc(ec2):
    ec2 = boto3.client('ec2')
    vpc = ec2.create_vpc(cidrBlock='10.0.0.0/16')['Vpc']
    vpc_id = vpc['VpcId']
    ec2.modify_vpc_attribute(VpcId=vpc_id , EnableDnsSupport={'Value: True'})
    ec2.modify_vpc_attribute(VpcId = vpc_id , EnableDnsHostnames={'Value: True'})
    return vpc_id


# Create subnets
def create_subnets(ec2 , vpc_id):
    pub_subnet = ec2.create_subnet( cidrBlock='10.0.1.0/24',VpcId=vpc_id, AvailabilityZone='us-east-1a')['Subnet']
    pri_subnet=ec2.create_subnet(cidrBlock='10.0.2.0/24',VpcId=vpc_id, AvailabilityZone='us-east-1a')['Subnet']
    return pub_subnet['SubnetId'], pri_subnet['SubnetId']

# Create Internet Gateway
def create_internet_gateway(ec2 , vpc_id):
    igw_id = ec2.create_internet_gateway()['InternetGateway']['InternetGatewayId']
    ec2.attached_internet_gateway(InternetGatewayId=igw_id , VpcId = vpc_id)
# Create Route table
def create_route_table(ec2 , vpc_id , pub_sub_id , priv_sub_id , igw_id , nat_gateway_id):
    # Create public Route
   pub_route =  ec2.create_route_table(VpcId=vpc_id)['RouteTable']
   ec2.create_route(RouteTableId = pub_route['RouteTableId'], DestinationCidrBlock= '0.0.0.0/0',GatewayId= igw_id)
   ec2.associate_route_table(RoutableId=pub_route['RouteTableId'] , subnetId=pub_sub_id)
   # Create Private Route
   priv_route = ec2.create_route_table(VpcId=vpc_id)['RouteTable']
   ec2.cretate_route(RouteTableId = priv_route['RouteTableId'] , DestinationCidrBlock='0.0.0.0/0', GatewayId = nat_gateway_id)
   ec2.associate_route_table(RouteTableId=priv_route['RouteTableId'] , subnetId = priv_sub_id)

# Create Key Pair
def cretate_key_pair(ec2):
    key_name = "my_key_pair"
    try:
        key = ec2.create_key_pair(keyName=key_name)
        # Create a file
        with open('my-key.pem' , 'w') as f:
            f.write(key['KeyMaterial'])
    except ec2.exception.ClientError:
        print("key already exists.")
    return key_name

# Create Security Group
def create_secrity_group(ec2 , vpc_id):
    sg_name = "my_security_group"
    sg_id = ec2.create_security_group(GroupName= sg_name , Description= 'allow ssh' , VpcId = vpc_id)['GroupId']
    ec2.authorize_security_group_ingress(GroupId=sg_id, IpProtocol='tcp', FromPort=22 , ToPort=22 ,cirdrIp='0.0.0.0/0' )
    return sg_id
# Create EC2 instance
def create_ec2(ec2 , ami,key_name , subnet_id , sg_id , associate_pub_ip):
    ec2_instance = ec2.run_instances(
    ImageId=ami ,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    Keyame=key_name,
    NetworkInterfaces = [{ 
        'SubnetId':subnet_id,
        'DeviceIndex': 0 ,
        'AssociatePublicIpAddress':associate_pub_ip,
        'Groups': [sg_id]
        }])['Instances'][0]
    return ec2_instance['InstancesId']
# Create a Nat Gateway
def create_nat_gateway(ec2 , pub_sub_id):
    eip = ec2.allocate_address(Domain='vpc')
    nat_gateway = ec2.create_nat_gateway(subnetId=pub_sub_id,AllocationId=eip['AllocationId']['NatGateway'])
    print("Waiting for the Nat Gateway to become available....")
    while True:
        state = ec2.describe_nat_gateways(NatGatewayIds=[nat_gateway['NatGatewayId']])['NatGateways'][0]['State']
        if state =="available":
            break
        time.sleep(0)
    return nat_gateway['NatGatewayId']

# Create Main Function
def main():
    ec2 = boto3.client("ec2")
    try:
        vpc_id = create_vpc(ec2)
        public_subnet_id = create_subnets(ec2 , vpc_id)
        private_subnet_id = create_subnets(ec2 , vpc_id)
        internet_gateway_id = create_internet_gateway(ec2 , vpc_id)
        key_name = cretate_key_pair(ec2)
        security_group_id = create_secrity_group(ec2 , vpc_id)
        ami = ""
        public_ec2_id = create_ec2(ec2 ,ami , key_name , public_subnet_id ,security_group_id,True )
        print(f"Public EC2 ID: {public_ec2_id}")
        nat_gateway_id = create_nat_gateway(ec2 , public_subnet_id)
        create_route_table(ec2 , vpc_id , public_subnet_id ,private_subnet_id , internet_gateway_id, nat_gateway_id)
        private_ec2_id  = create_ec2(ec2 , ami , key_name, private_subnet_id, security_group_id,False)
        print(f"Private EC2 ID: {private_ec2_id}")
        print("Setup complete")
    except Exception as e:
        print(f"Error during setup:  {e}")
        
    
