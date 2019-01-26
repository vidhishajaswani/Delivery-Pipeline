import boto3
ec2 = boto3.client('ec2', region_name='us-east-1')
#instance_id='i-0a92571745285734c'
response = ec2.terminate_instances(InstanceIds=[instance_id], DryRun=False)
print(response)
