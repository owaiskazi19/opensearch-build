# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import tempfile
import shutil

class GitClone:
    def __init__(self, url, directory = None):
        self.url = url
        if directory is None:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.dir = self.temp_dir.name
        else:
            self.dir = directory
            print(f'Deleting {self.dir}')
            shutil.rmtree(self.dir, ignore_errors = True)
            os.makedirs(self.dir, exist_ok = True)
        # https://owaiskazi19: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@github.com/owaiskazi19/opensearch-infra
        self.execute(f'git clone {self.url}', True)
    

    def execute(self, command, silent = False):
        print(f'Executing "{command}" in {self.dir}')
        if silent:
            subprocess.check_call(command, cwd = self.dir, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        else:
            subprocess.check_call(command, cwd = self.dir, shell = True)