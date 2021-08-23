import os
import subprocess
import sys
from pathlib import Path

class PerformanceTestSuite:
    def __init__(self, bundle_manifest):
        self.manifest = bundle_manifest
        self.work_dir = '/opensearch/tools/cdk/mensor/mensor_tests'
        self.mensor_dir = '/opensearch/mensor-py-client'

    
    def execute(self, cluster, current_dir, python_path):
        print(os.listdir())
        print(os.getcwd())
        # root_dir = Path(os.getcwd()).parent.parent.parent.parent
        # print(root_dir)
        #current_path = Path(os.getcwd())
        #print(current_path.parent)
        #print(os.listdir())
        #os.chdir('opensearch')
        #print(os.listdir)

        # #Set PYHTONPATH variable
        # path_to_mensor_sdk = current_dir + self.mensor_dir
        # print(path_to_mensor_sdk)
        # #subprocess.check_call(f'export PYTHONPATH="$PYTHON{path_to_mensor_sdk}"', cwd=dir, shell=True)
        # #print("subprocess", os.environ)
        # sys.path.append(path_to_mensor_sdk)
        # print(sys.path)
     
        # os.environ['PYTHONPATH'] = path_to_mensor_sdk
        
        # print("env", os.environ)

        # os.chdir(os.getcwd()+ self.work_dir)
        #print (os.environ)
        print(python_path)
        sys.path.append(python_path)
        print(sys.path)
        
        # print(os.listdir())
        os.chdir(self.work_dir)
        print(os.listdir())
        dir = os.getcwd()
       
        #Install the depedencies
        subprocess.check_call('pip3 install boto3 requests setuptools retry dataclasses_json', cwd=dir, shell=True)

        

        subprocess.check_call(f'python3 test_config.py -i 172.31.50.10 -b 12212 -a {self.manifest.build.architecture} -s', cwd=dir, shell=True)
