import boto3
import os
import json

os.environ['AWS_PROFILE'] = "Francis"
os.environ['AWS_DEFAULT_REGION'] = "us-west-2"

eb_env = boto3.client('elasticbeanstalk')
ec2 = boto3.client('ec2')
ALB = boto3.client('elbv2')

app_name='docker-no-alb'

# Create a VPC with a specified CIDR block
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16', InstanceTenancy='default', DryRun=False)
print(f"{vpc['Vpc']['VpcId']} created successfully")


# Enable DNS hostnames for the VPC
ec2.modify_vpc_attribute(VpcId=vpc['Vpc']['VpcId'], EnableDnsSupport={'Value': True})
ec2.modify_vpc_attribute(VpcId=vpc['Vpc']['VpcId'], EnableDnsHostnames={'Value': True})

# create and associate an elastic Ip address
# eipalloc = ec2.allocate_address(
# 	Domain='vpc',
# )

# Create an Internet Gateway and attach it to the VPC
igw = ec2.create_internet_gateway(DryRun=False)
ec2.attach_internet_gateway(InternetGatewayId=igw['InternetGateway']['InternetGatewayId'], VpcId=vpc['Vpc']['VpcId'])

# Create a custom route table
rtb = ec2.create_route_table(
	VpcId=vpc['Vpc']['VpcId'],
)

# Create a route to the internet-gateway
ec2.create_route(
	DestinationCidrBlock='0.0.0.0/0',
	GatewayId=igw['InternetGateway']['InternetGatewayId'],
	RouteTableId=rtb['RouteTable']['RouteTableId']
)

# Create 4 public & Private subnets (two in each availability zone)
subnets={}

for i in range(1,5):
	az = "us-west-2a" if i % 2 == 1 else "us-west-2b"
	subnet = ec2.create_subnet(VpcId=vpc['Vpc']['VpcId'], CidrBlock=f'10.0.{i}.0/24', AvailabilityZone=az, DryRun=False)
	subnet_id=subnet['Subnet']['SubnetId']

	# Associate subnets with route tables
	ec2.associate_route_table(SubnetId=subnet_id, RouteTableId=rtb['RouteTable']['RouteTableId']) 
	subnets[subnet_id] = az

print(f"Subnets: {json.dumps(subnets, indent=4, sort_keys=True, default=str)}")

# Get all unique availability zones
availability_zones = set(subnets.values())

# Initialize empty lists to store subnet IDs from different zones
subnet_ids_zone1 = []
subnet_ids_zone2 = []

# Iterate through the dictionary and distribute subnet IDs based on zones
for subnet_id, zone in subnets.items():
    if zone in availability_zones:
        availability_zones.remove(zone)  # Remove zone from set after adding a subnet from it
        if subnet_ids_zone1:
            subnet_ids_zone2.append(subnet_id)
        else:
            subnet_ids_zone1.append(subnet_id)

# Create a NAT Gateway in one of the public subnets
# nat_gateway = ec2.create_nat_gateway(SubnetId=subnet_ids[0], AllocationId=eipalloc['AllocationId'], DryRun=False)

# Create a security group allowing inbound traffic on port 8501
security_group = ec2.create_security_group(
	GroupName='MySecurityGroup',
	Description='Allow inbound traffic on port 8501',
	VpcId=vpc['Vpc']['VpcId'],
	DryRun=False
)
print(f"Security Group ID: {security_group['GroupId']}")

ec2.authorize_security_group_ingress(
	GroupId=security_group['GroupId'],
	IpPermissions=[
		{'IpProtocol': 'tcp', 'FromPort': 8501, 'ToPort': 8501, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
	]
)


# # create an application loadbalancer
# elb = ALB.create_load_balancer(
# 	Name=f'{app_name}-elb',
# 	Subnets=[
# 		subnet_ids_zone1[0],
# 		subnet_ids_zone2[0]
# 	],
# 	SecurityGroups=[security_group['GroupId']],
# 	Scheme='internet-facing'
# )

# print(f"LoadBalancer: {elb['LoadBalancers'][0]['LoadBalancerArn']}")
# # print()

# # Create a target group
# target_grp = ALB.create_target_group(
#     Name='my-target-group',
#     Protocol='HTTP',
#     Port=80,
#     VpcId=vpc['Vpc']['VpcId'],
# )

# print(f"Target group created: {target_grp['TargetGroups'][0]['TargetGroupArn']}")

# # Create a listener for HTTP traffic
# ALB.create_listener(
#     LoadBalancerArn=elb['LoadBalancers'][0]['LoadBalancerArn'],
#     Protocol='HTTP',
#     Port=80,
#     DefaultActions=[{
#         'Type': 'forward',
#         'TargetGroupArn': target_grp['TargetGroups'][0]['TargetGroupArn']
#     }]
# )


# create Elastic beanstalk application
try:
	app = eb_env.create_application(
		ApplicationName = app_name
	)
except Exception as e:
	print("Application exists")
# print(app)

# Create environment
env = eb_env.create_environment(
	ApplicationName=app_name,
	EnvironmentName = f"{app_name}-env",
	Tier = {
		'Name': 'WebServer',
		'Type': 'Standard'
	},
	SolutionStackName = '64bit Amazon Linux 2023 v4.2.2 running Docker',
	OptionSettings=[
		{
			'Namespace': 'aws:autoscaling:launchconfiguration',
			'OptionName': 'IamInstanceProfile',
			'Value': 'aws-elasticbeanstalk-ec2-role'
		},
		{
			'Namespace': 'aws:ec2:vpc',
			'OptionName': 'VPCId',
			'Value': vpc['Vpc']['VpcId']
		},
		{
			'Namespace': 'aws:ec2:vpc',
			'OptionName': 'Subnets',
			'Value': ','.join(list(subnets.keys()))
		},
		{
			'Namespace': 'aws:elasticbeanstalk:environment',
            'OptionName': 'EnvironmentType',
            'Value': 'SingleInstance'
		}

	]
)
print(f"Launching Environment: {env['EnvironmentId']}")
# print(json.dumps(env, indent=4, sort_keys=True, default=str))