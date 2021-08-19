import os
import argparse
import yaml
from git.git_repository import GitRepository
from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_cluster import PerformanceTestCluster
from test_workflow.perf_test_suite import PerformanceTestSuite
from system.temporary_directory import TemporaryDirectory

parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help = "Manifest file.")
parser.add_argument('--keep', dest = 'keep', action='store_true', help = "Do not delete the working temporary directory.")
parser.add_argument('--stack', dest = 'stack', help = 'Stack name for performance test')
parser.add_argument('config', type = argparse.FileType('r'), help = "Config file.")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)

config = yaml.load(args.config, Loader=yaml.FullLoader)


with TemporaryDirectory(keep = args.keep) as work_dir:
    os.chdir(work_dir)
    
    #Spin up a single node cluster for performance test
    cloned_repo = GitRepository('https://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:x-oauth-basic@github.com/opensearch-project/opensearch-infra', 'main', 'opensearch')
    perf_cluster = PerformanceTestCluster(manifest, config, args.stack)
    perf_cluster.create()

    perf_test_suite = PerformanceTestSuite(manifest)
    perf_test_suite.execute(perf_cluster)
