#References : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-examples.html

import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

# Create a Key Pair that will be linked to our Instance
outfile = open('aws-key.pem','w')
key_pair = ec2.create_key_pair(KeyName='aws-key')
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)

# Create Virtual Private Cloud
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/24')

subnet = vpc.create_subnet(CidrBlock='10.0.0.0/25')
gateway = ec2.create_internet_gateway()
gateway.attach_to_vpc(VpcId=vpc.id)
route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=gateway.id
)
route_table.associate_with_subnet(SubnetId=subnet.id)


#A security group acts as a virtual firewall that controls the traffic for one or more instances. 
sec = ec2.create_security_group(
    GroupName='aws-ssh', Description='vidhisha sec group', VpcId=vpc.id)
sec_group=sec.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
)

# Finally create instance by giving the Image ID and Instance Type
instances = ec2.create_instances(
    ImageId='ami-035be7bafff33b6b6', InstanceType='t2.micro', MaxCount=1, MinCount=1,KeyName="aws-key",
    NetworkInterfaces=[{'SubnetId': subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec.group_id]}])

#instances[0].id
print(instances)
print("Instance Created Successfully")

