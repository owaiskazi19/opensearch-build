import os
import subprocess
import sys
from pathlib import Path

class PerformanceTestSuite:
    def __init__(self, bundle_manifest):
        self.manifest = bundle_manifest
        self.work_dir = '/mensor_tests/'

    
    def execute(self, cluster):
        
        root_dir = Path(os.getcwd()).parent.parent.parent.parent
        print(root_dir)
        current_path = Path(os.getcwd())
        print(current_path.parent)
        
        os.chdir(str(current_path.parent) + self.work_dir)
        
  
        dir = os.getcwd()
       
        #Install the depedencies
        subprocess.check_call('pip3 install boto3 requests setuptools retry', cwd=dir, shell=True)

        #Set PYHTONPATH variable
        sys.path.append(str(root_dir) + '/mensor-py-client/mensor')

        subprocess.check_call(f'python3 test_config.py -i {cluster.endpoint()} -b 12212 -a {self.manifest.build.architecture}', cwd=dir, shell=True)
