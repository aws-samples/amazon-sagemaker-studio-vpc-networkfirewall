# Amazon SageMaker Studio demo

# Overview

![Amazon SageMaker Studio infrastructure overview](design/sagemaker-studio-vpc.drawio.svg)

## VPC resources

## S3 resources

The solution deploys two Amazon S3 buckets: 
- `<project_name>-data`  
- `<project_name>-models`

Both buckets have a bucket policy attached. The bucket policy explicitly denies all access to the bucket which does not come from the designated VPC endpoint:
```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::sagemaker-studio-vpc-data/*",
                "arn:aws:s3:::sagemaker-studio-vpc-data"
            ],
            "Condition": {
                "StringNotEquals": {
                    "aws:sourceVpce": "vpce-030d2a4225078681a"
                }
            }
        }
    ]
}
```

The Amazon S3 VPC endpoint has a policy attached to it. This policy allows access the the two S3 buckets (`model` and `data`) only:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::sagemaker-studio-vpc-data",
                "arn:aws:s3:::sagemaker-studio-vpc-models",
                "arn:aws:s3:::sagemaker-studio-vpc-data/*",
                "arn:aws:s3:::sagemaker-studio-vpc-models/*"
            ]
        }
    ]
}
```

This combination of S3 bucket policy and VPC endpoint policy, together with Amazon SageMaker Studio VPC connectivity, establishes that SageMaker Studio can only access the referenced S3 bucket, and this S3 bucket can only be accessed from the VPC endpoint.

❗ You will not be able to access these S3 buckets from the AWS console.

## IAM resources


# Deployment

## Prerequisites
- An AWS Account
- An IAM user or role with administrative access
- configured `aws cli` with that IAM user or role credentials

## CloudFormation stack parameters
- `ProjectName`: **OPTONAL**. Default is `sagemaker-studio-vpc`
- `VpcCIDR`: **OPTONAL**. Default is 10.2.0.0/16
- `FirewallSubnetCIDR`: **OPTONAL**. Default is 10.2.1.0/24
- `NATGatewaySubnetCIDR`: **OPTONAL**. Default is 10.2.2.0/24
- `SageMakerStudioSubnetCIDR`: **OPTONAL**. Default is 10.2.3.0/24

You can change the stack parameters in the `Makefile`.

❗ Please make sure that default or your custom CIDRs do not conflict with any existing VPC in the account and the region where you are deploying the CloudFormation stack

## Deployment steps

To deploy the stack into the current account and region:

### Deploy CloudFormation stack
```bash
make deploy
```

**Temporary fix**: 
1. Add the route to the Firewall VPC endpoint to the Internet Gateway route table:
```bash
DEST_CIDR=10.2.2.0/24
FIREWALL_VPCE=vpce-0df2998d6ec900ccc
IGW_RTB=rtb-097a3cafaa421ddcc

aws ec2 create-route \
    --destination-cidr-block ${DEST_CIDR} \
    --vpc-endpoint-id ${FIREWALL_VPCE} \
    --route-table-id ${IGW_RTB}
```

2. Add the route to the Firewall VPC endpoint to the NAT Gateway route table:
```bash
DEST_CIDR=0.0.0.0/0
FIREWALL_VPCE=vpce-0df2998d6ec900ccc
NATGW_RTB=rtb-0d226d36fc7cdd662

aws ec2 create-route \
    --destination-cidr-block ${DEST_CIDR} \
    --vpc-endpoint-id ${FIREWALL_VPCE} \
    --route-table-id ${NATGW_RTB}
```
  
### Create an Amazon SageMaker Studio domain inside a VPC
```bash
# Please replace the variable below according to your environment
REGION=eu-west-1 # AWS Region where the Domain will be created
VPC_DOMAIN_NAME= # Select a name for your Domain

# The values below can be obtained on the "Output" section of the CloudFormation used on the previous step
VPC_ID=
SAGEMAKER_STUDIO_SUBNET_IDS=
SAGEMAKER_SECURITY_GROUP=
EXECUTION_ROLE_ARN=

aws sagemaker create-domain \
    --region $REGION \
    --domain-name $VPC_DOMAIN_NAME \
    --vpc-id $VPC_ID \
    --subnet-ids $SAGEMAKER_STUDIO_SUBNET_IDS \
    --app-network-access-type VpcOnly \
    --auth-mode IAM \
    --default-user-settings "ExecutionRole=${EXECUTION_ROLE_ARN},SecurityGroups=${SAGEMAKER_SECURITY_GROUP}"

#Please note the DomainArn output - we will use it on the next step
```


# SageMaker security
 
## SageMaker-related approaches for security, access control and restriction

## Network isolation

## Access to resources in VPC

## Deploy SageMaker Studio to VPC

## Amazon S3 access control

## Limit internet ingress and egress

## Secure configuration of SageMaker notebook instances

## Enforce secure deployment of SageMaker resources



# Resources
[1]. [SageMaker Security](https://docs.aws.amazon.com/sagemaker/latest/dg/security.html)  
[2]. [SageMaker Infrastructure Security](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-security.html)  
[3]. I took the initial version of the CloudFormation templates for deployment of VPC, Subnets and S3 buckets from this [GitHub repository](https://github.com/aws-samples/amazon-sagemaker-studio-vpc-blog)  
[4]. Blog post for the [1] repository: [Securing Amazon SageMaker Studio connectivity using a private VPC](https://aws.amazon.com/blogs/machine-learning/securing-amazon-sagemaker-studio-connectivity-using-a-private-vpc/)  
[5]. [Secure deployment of Amazon SageMaker resources](https://aws.amazon.com/blogs/security/secure-deployment-of-amazon-sagemaker-resources/)  
[6]. Security-focused workshop [Amazon SageMaker Workshop: Building Secure Environments](https://sagemaker-workshop.com/security_for_sysops.html)  
[7]. [Amazon SageMaker Identity-Based Policy Examples](https://docs.aws.amazon.com/sagemaker/latest/dg/security_iam_id-based-policy-examples.html)  
[8]. [Deployment models for AWS Network Firewall](https://aws.amazon.com/blogs/networking-and-content-delivery/deployment-models-for-aws-network-firewall/)  
[9]. [VPC Ingress Routing – Simplifying Integration of Third-Party Appliances](https://aws.amazon.com/blogs/aws/new-vpc-ingress-routing-simplifying-integration-of-third-party-appliances/)  