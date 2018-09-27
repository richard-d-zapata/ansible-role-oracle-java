import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java_version_file(host):
    f = host.file('/tmp/java_version')

    assert f.exists
    assert f.contains("11\n")


def test_java_installer_filename_file(host):
    f = host.file('/tmp/java_installer_filename')

    assert f.exists
    assert f.contains("jdk-11_linux-x64_bin.tar.gz\n")
