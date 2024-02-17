import boto3
import os
import json

os.environ['AWS_PROFILE'] = "Francis"
os.environ['AWS_DEFAULT_REGION'] = "us-west-2"

eb_env = boto3.client('elasticbeanstalk')
ec2 = boto3.client('ec2')
ALB = boto3.client('elb')


# Release Elastic Ip address to Ip pool (Delete)
releaseIpAdd = ec2.release_address(
    AllocationId= #read from text file
)