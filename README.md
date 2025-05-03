# I - S3 Unsecured Buckets Checker
his Python script scans all S3 buckets in an AWS account and lists those that:

 - Do not have server-side encryption enabled.

 - Do not have a bucket policy applied.

## Features 
 - Scans all S3 buckets in your AWS account.

 - Checks for missing encryption settings.

 - Checks for missing bucket policies.

 - Provides a list of unsecured buckets.

 # II - S3 Bucket Security Enhancer
 This Python script secures all S3 buckets in an AWS account by:

 - Enabling **server-side encryption (AES256)**.

 - Applying a **bucket policy** to enforce HTTPS-only access.

 ### Features
   - Enables AES256 encryption for all buckets.

  - Applies a bucket policy that enforces HTTPS-only access.

 - Uses Boto3 to interact with AWS S3.


 # III - AWS Identity and Access Management (IAM)
 # 🛡️ AWS IAM Lab with Python

This lab demonstrates the basics of **AWS Identity and Access Management (IAM)** using Python and Boto3. It walks you through how to:

- ✅ Create an IAM group
- ✅ Attach a policy to the group
- ✅ Create an IAM user
- ✅ Add the user to the group

![alt text](projects/iam/image.png)

## 📦 Requirements

- Python 3.x
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- Configured AWS CLI credentials with appropriate IAM permissions

Install Boto3 if you haven't already:

```
pip install boto3
```
# IV - AWS VPC Setup with Boto3
This project automates the setup of a Virtual Private Cloud (VPC) environment in AWS using Python and Boto3. It includes:
- Creation of a VPC, public and private subnets
- Internet and NAT Gateway configuration
- Route tables and security groups
- EC2 instance provisioning in both subnets
## ✅ Result
- Public EC2: Internet accessible
- Private EC2: Internet access via NAT Gateway
- SSH verified on Public EC2
## 🧹 Cleanup
To avoid ongoing charges, make sure to delete:
- EC2 instances
- NAT Gateway
- EIP
- Subnets
- VPC

