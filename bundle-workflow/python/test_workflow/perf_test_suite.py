import os
import subprocess
import sys
from pathlib import Path

class PerformanceTestSuite:
    def __init__(self, bundle_manifest, endpoint, security):
        self.manifest = bundle_manifest
        self.work_dir = 'tools/cdk/mensor/mensor_tests'
        self.endpoint = endpoint
        self.security = security

    
    def execute(self):
        
        #Append PYTHONPATH
        #sys.path.append(os.getenv('PYTHONPATH'))
        
        os.chdir(self.work_dir)
        dir = os.getcwd()
       
        if self.security:
            subprocess.check_call(f'python3 test_config.py -i {self.endpoint} -b 12212 -a {self.manifest.build.architecture} -s', cwd=dir, shell=True)
        else:
            subprocess.check_call(f'python3 test_config.py -i {self.endpoint} -b 12212 -a {self.manifest.build.architecture}', cwd=dir, shell=True)
        