import os
import tempfile
import urllib.request
import shutil
import subprocess
import json

class PerformanceTestCluster:
    def __init__(self, bundle_manifest, stack_name):
        self.manifest = bundle_manifest
        self.work_dir = 'opensearch/opensearch-infra/tools/cdk/mensor/single-node/'
        self.stack_name = stack_name
        self.output_file = 'output.json'
        self.ip_address = ''

    def create(self):       
        os.chdir(self.work_dir)
        dir = os.getcwd()
        
        command = f'cdk deploy --all -c url={self.manifest.build.location} -c security_group_id=sg-0368b2d37e229645b -c vpc_id=vpc-f6b57d8f -c account_id=724293578735 -c region=eu-west-1 -c stack_name={self.stack_name} -c security=disable -c architecture={self.manifest.build.architecture} --profile infra --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
        print(os.listdir())
        with open('output.json', 'r') as read_file:
            load_output = json.load(read_file)
        self.ip_address = load_output[self.stack_name]['PrivateIp']
        print('Private IP:', self.ip_address)

    def endpoint(self):
        return self.ip_address

    def port(self):
        return 9200

    def destroy(self):
        command = f'cdk destroy --all -c url={self.manifest.build.location} -c security_group_id=sg-0368b2d37e229645b -c vpc_id=vpc-f6b57d8f -c account_id=724293578735 -c region=eu-west-1 -c stack_name={self.stack_name} -c security=disable -c architecture={self.manifest.build.architecture} --profile infra --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
