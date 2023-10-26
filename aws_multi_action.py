import boto3
import uuid
from pprint import pprint

#Access key: #AKIAY4ZUXA4AIUPYA7NV
#Secret key: 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

# BOTO3 Documentation:
#https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

class IAMUserManager:
    def __init__(self):
        self.region = "us-east-1"
        #Open management console
        self.session = boto3.session.Session(profile_name="default", region_name=self.region)
        # Open IAM console
        self.iam_console_resource = self.session.resource("iam") #Resource object: Higher Level Object oriented service access where output can be a simpler list.
        self.iam_console_client = self.session.client("iam") #Client object: Low Level Service Access where output is dictionary which needs more effort.
    # Example of how to do it with lambda
    def get_users_lambda(self):
        users = map(lambda user: user.name, self.iam_console_resource.users.all())
        return list(users)

    #Example of IAM users list with resource object
    def pull_user(self):
        for each_user in self.iam_console_resource.users.all():
            print(each_user.name)
    #Example of IAM users list with client object
    def pull_user1(self):
        for each_user1 in self.iam_console_client.list_users()['Users']:
            print(each_user1['UserName'])
    #Example of how to pull all list users
    def pull_user2(self):
        list_users1 = self.iam_console_client.list_users()
        for user1 in list_users1['Users']:
            pprint(user1['UserName'])
class EC2Manage(IAMUserManager):
    def __init__(self):
        super().__init__()
        #Open EC2 Console
        self.ec2_console = self.session.client(service_name="ec2") 
        ec2 = boto3.resource("ec2",region_name=self.region)
        
    # List ec2 instances
    def get_ec2(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html
        response = self.ec2_console.describe_instances()['Reservations']
        instances_ids = []
        for instance in response:
            for value in instance['Instances']:
                instances_ids.append(value['InstanceId'])
        return instances_ids

    # Reads VMs names from a file
    def read_ec2(self):
        f =open("ec2_names.txt","r")
        ec2_names = f.readlines()
        self.ec2_list = []
        for name in ec2_names:
            self.ec2_list.append(name.strip())
        return self.ec2_list
    # Create EC2 instances from file
    def create_ec2(self):
        read_ec2_names = self.read_ec2()
        for read_ec2_name in read_ec2_names:  
            response = self.ec2_console.run_instances(
                ImageId='ami-067d1e60475437da2',
                InstanceType='t2.micro',
                MaxCount=1,
                MinCount=1,  # Add a comma here
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': read_ec2_name
                            },
                        ]
                    },
                ]
            )
        
    # Stop EC2s
    def stop_ec2s(self):
        ec2_ids = self.get_ec2()
        for ec2_id in ec2_ids:
            response = self.ec2_console.stop_instances(InstanceIds=[ec2_id])
            print(f"Stopping instance {ec2_id} ")
    # Terminate EC2s
    def terminate_ec2(self):
        ec2_ids = self.get_ec2()
        for ec2_id in ec2_ids:
            response = self.ec2_console.terminate_instances(InstanceIds=[ec2_id])
            print(f"Terminating instance {ec2_id} ")

class S3Manager(IAMUserManager):
    def __init__(self):
        super().__init__()
        # Open S3 connection
        self.s3_connection = boto3.client("s3", region_name=self.region)
    def get_s3_buckets(self):
        self.contain_buckets = []
        self.bucket_list = self.s3_connection.list_buckets()
        for name_bucket in self.bucket_list['Buckets']:
            self.contain_buckets.append(name_bucket["Name"])
        return self.contain_buckets
    def delete_bucket(self):
        self.bucket_list = self.get_s3_buckets()
        for name_bucket in self.bucket_list:
            self.bucket_deleted = self.s3_connection.delete_bucket(Bucket= name_bucket)
            print("Bucket: ", self.bucket_deleted, "deleted successfully")
    def generate_bucket_name(self):
        # The generated bucket name must be between 3 and 63 chars long
        bucket_prefix = "bran-" + str(uuid.uuid4())
        return bucket_prefix
    def create_bucket(self):
        get_name = self.generate_bucket_name()
        self.bucket_name = get_name 
        self.s3_connection.create_bucket(Bucket=self.bucket_name)
        print(self.bucket_name)

boto = S3Manager()
# S3
#print(boto.generate_bucket_name())
#boto.create_bucket()
list_buckets1 = boto.get_s3_buckets()
for bcket in list_buckets1:
    print("Bucket Name: ",bcket)
#boto.delete_bucket()
# EC2
#get_list_ec2s = boto.get_ec2()
#for i in get_list_ec2s:
#    print(i)
#boto.create_ec2()
#boto.stop_ec2s()
#boto.terminate_ec2()
#print(boto.pull_user1())
