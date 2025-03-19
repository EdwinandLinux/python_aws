import boto3
def get_unencrypted_buckets():
    s3 = boto3.client("s3")
    unencrypted_buckets =[]
    #encrypted_buckets =[]
    try:
        buckets = s3.list_buckets()["Buckets"]
        for bucket in buckets:
            bucket_name=bucket['Name']
            # Check for encryption
            try:
                s3.get_bucket_encryption(Bucket=bucket_name)
                #encrypted_buckets.append(bucket_name)
            except s3.exceptions.ClientError as e:
                if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
                    unencrypted_buckets.append(bucket_name)

 
    except Exception as e:
        print (f"Error fetching buckets: {e}")
    return unencrypted_buckets

def get_buckets_with_no_policy():
    s3 = boto3.client('s3')
    buckets_without_policy= []
    #buckets_with_policy= []
    try:
        buckets = s3.list_buckets()["Buckets"]
        for bucket in buckets:
            bucket_name = bucket["Name"]
            try:
                s3.get_bucket_policy(Bucket=bucket_name)
                #buckets_with_policy.append(bucket_name)
            except s3.exceptions.ClientERROR as e:
                if "NoSuchBucketPolicy" in str(e):
                    buckets_without_policy.append(bucket_name)


    except Exception as e:
        print(f"Error fetching bucket policies: {e}")
    return buckets_without_policy

if __name__ =="__main__":
    unencrypted_buckets =get_unencrypted_buckets()  
    buckets_with_no_policy = get_buckets_with_no_policy()
    print(f"Buckets without Encryption Enabled:")
    print(unencrypted_buckets)
    print("\n")
    print(f"Buckets with No Bucket Policy Applied:")
    print(buckets_with_no_policy)
    #print("###############")
    #encrypted_buckets =get_unencrypted_buckets()  
   # buckets_with_policy = get_buckets_with_no_policy()
   # print(f"Buckets with Encryption Enabled:")
    #print(encrypted_buckets)
    #print("\n")
    #print(f"Buckets with Bucket Policy Applied:")
    #print(buckets_with_policy)


