import os
import argparse
import yaml
import subprocess
from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_cluster import PerformanceTestCluster
from test_workflow.perf_test_suite import PerformanceTestSuite
from system.temporary_directory import TemporaryDirectory

parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help = "Manifest file.")
parser.add_argument('--keep', dest = 'keep', action='store_true', help = "Do not delete the working temporary directory.")
parser.add_argument('--stack', dest = 'stack', help = 'Stack name for performance test')
parser.add_argument("--security", dest="security", action='store_true', help = "Security of the cluster should be True/False")
parser.add_argument('config', type = argparse.FileType('r'), help = "Config file.")
parser.add_argument('-p', dest = 'p', help = 'PYTHONPATH')
#REMOVE THIS
parser.add_argument("-t", '--token', help="Github Token")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)

config = yaml.load(args.config, Loader=yaml.FullLoader)

workspace = os.getcwd()


with TemporaryDirectory(keep = args.keep) as work_dir:
    # current_dir = os.getcwd()
    #print(os.listdir())
    print("workspace", workspace)
    os.chdir(workspace)
    #print(os.listdir())
    #Spin up a single node cluster for performance test
    print(os.getenv('WORKSPACE'))
    current_workspace = os.path.join(workspace, 'infra18')
    cloned_repo = GitRepository(f'https://{args.token}:x-oauth-basic@github.com/opensearch-project/opensearch-infra', 'main', current_workspace)

    print(os.listdir())
    current_dir = os.getcwd()
    print(current_dir)
    #os.chdir(os.getenv('WORKSPACE'))
 
    print(os.chdir(current_workspace))
 
    print(os.getcwd())
    print(os.listdir())
    security = True if args.security else False
    # perf_cluster = PerformanceTestCluster(manifest, config, args.stack, security)
    # perf_cluster.create()

    #os.chdir(work_dir)
    #mensor_sdk_path = root_dir + current_dir
    perf_test_suite = PerformanceTestSuite(manifest)
    perf_test_suite.execute(None, current_dir, args.p)
