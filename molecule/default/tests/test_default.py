import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java_version_file(host):
    f = host.file('/tmp/java_version')

    assert f.exists
    assert f.contains("11\n")
