#!/bin/bash
# Cloudformation parameters
REGION="us-east-1"
STACK_NAME="test-stack"
APP_NAME="my-app"
VPC_ID="vpc-01234567890123456"
# Subnets must be in different AZs
SUBNET_A="subnet-01234567890123456"
SUBNET_B="subnet-01234567890123456"
HOSTED_ZONE_NAME="example.com"
SUBDOMAIN="www"
SSL_CERT_ARN='arn:aws:acm:region:123456789012:certificate/00000000-0000-0000-0000-000000000000'
IMAGE_URI='123456789012.dkr.ecr.region.amazonaws.com/image:tag'
# Role needed for ECS to be able to perform tasks (pull images, etc.)
ecsTaskExecutionRoleArn=$(aws iam get-role --role-name ecsTaskExecutionRole | python -c "import sys, json; print(json.load(sys.stdin)['Role']['Arn'])")

# Request a cert if a valid cert is not specified.
# The cert is validated through DNS.
if [[ ! $SSL_CERT_ARN  ]]; then
  SSL_CERT_ARN=$(./request_cert.py $HOSTED_ZONE_NAME)
fi

aws cloudformation create-stack --region ${REGION} --stack-name ${STACK_NAME} \
--template-body file://ecs_app.yaml \
--parameters \
ParameterKey=ApplicationName,ParameterValue=${APP_NAME} \
ParameterKey=VPC,ParameterValue=${VPC_ID} \
ParameterKey=SubnetA,ParameterValue=${SUBNET_A} \
ParameterKey=SubnetB,ParameterValue=${SUBNET_B} \
ParameterKey=HostedZoneName,ParameterValue=${HOSTED_ZONE_NAME} \
ParameterKey=Subdomain,ParameterValue=${SUBDOMAIN} \
ParameterKey=SSLCert,ParameterValue=${SSL_CERT_ARN} \
ParameterKey=ImageURI,ParameterValue=${IMAGE_URI} \
ParameterKey=EcsTaskExecutionRoleArn,ParameterValue=${ecsTaskExecutionRoleArn}
