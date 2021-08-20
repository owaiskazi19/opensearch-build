import os
import subprocess
import json
import yaml
from aws_requests_auth.aws_auth import AWSRequestsAuth
import boto3
from test_workflow.test_cluster import TestCluster

class PerformanceTestCluster(TestCluster):
    def __init__(self, bundle_manifest, config, stack_name, security):
        self.manifest = bundle_manifest
        self.security_id = config['Constants']['SecurityGroupId']
        self.vpc_id = config['Constants']['VpcId']
        self.account_id = config['Constants']['AccountId']
        self.region = config['Constants']['Region']
        self.work_dir = 'opensearch/tools/cdk/mensor/single-node/'
        self.stack_name = stack_name
        self.output_file = 'output.json'
        self.ip_address = None
        self.security = security

    def create(self):
        os.chdir(self.work_dir)
        dir = os.getcwd()

        security = 'disable'
        if self.security:
            security = 'enable'

        # boto3.set_stream_logger('')
        # Get the built-in boto3 client for STS
        sts_client = boto3.client('sts')

        # Assume the Infra Testing Account
        sts_credentials = sts_client.assume_role(
        RoleArn="arn:aws:iam::724293578735:role/cfn-set-up",
        RoleSessionName="Spin-up-performance-test-cluster",
        DurationSeconds=3600)['Credentials']


        assumed_role_session = boto3.Session(
            aws_access_key_id=sts_credentials['AccessKeyId'],
            aws_secret_access_key=sts_credentials['SecretAccessKey'],
            aws_session_token=sts_credentials["SessionToken"],
            #aws_region=self.region,
        )

        # authorization = AWSRequestsAuth(aws_access_key=sts_credentials['AccessKeyId'],
        #                             aws_secret_access_key=sts_credentials['SecretAccessKey'],
        #                             aws_token=sts_credentials['SessionToken'],
        #                             #aws_host=MENSOR_ENDPOINT,
        #                             aws_region=self.region,
        #                             aws_service='cluster')

        command = f'cdk deploy --all -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id} -c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security={security} -c architecture={self.manifest.build.architecture} --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
        with open(self.output_file, 'r') as read_file:
            load_output = json.load(read_file)
        self.ip_address = load_output[self.stack_name]['PrivateIp']
        print('Private IP:', self.ip_address)

    def endpoint(self):
        return self.ip_address

    def port(self):
        if self.security:
            return 443
        return 9200

    def destroy(self):
        security = 'disable'
        if self.security:
            security = 'enable'

        command = f'cdk destroy --all -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id} -c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security={security} -c architecture={self.manifest.build.architecture} --profile infra --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
