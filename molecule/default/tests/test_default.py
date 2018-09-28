import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java_version_file(host):
    f = host.file('/tmp/java_version')
    assert f.exists
    assert f.contains("11\n")


def test_java_installer_filename_file(host):
    if host.system_info.distribution == "ubuntu":
        ext = "tar.gz"
    elif host.system_info.distribution == "centos":
        ext = "rpm"
    f = host.file('/tmp/java_installer_filename')
    assert f.exists
    assert f.contains("jdk-11_linux-x64_bin." + ext + "\n")


def test_installer_exists(host):
    if host.system_info.distribution == "ubuntu":
        ext = "tar.gz"
    elif host.system_info.distribution == "centos":
        ext = "rpm"
    f = host.file("/tmp/jdk-11_linux-x64_bin." + ext)
    assert f.exists


def test_java_version(host):
    result = host.run("java -version")
    assert "\"11\"" in result.stderr
