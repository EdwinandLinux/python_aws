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