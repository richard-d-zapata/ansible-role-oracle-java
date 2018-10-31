import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def get_java_version():
    return os.getenv('JAVA_VERSION', '11.0.1')


@pytest.fixture(scope='module')
def test_vars(host):
    java_version = get_java_version()
    java_version_parts = java_version.split('.')
    if int(java_version_parts[0]) > 8:
        java_version_feature = java_version_parts[0]
        if len(java_version_parts) > 1:
            java_version_interim = java_version_parts[1]
        else:
            java_version_interim = '0'
        if len(java_version_parts) > 2:
            java_version_update = java_version_parts[2]
        else:
            java_version_update = '0'
        if len(java_version_parts) > 3:
            java_version_patch = java_version_parts[3]
        else:
            java_version_patch = '0'
        java_version = ''
        if int(java_version_patch) > 0:
            java_version = '.' + java_version_patch
        if (int(java_version_update) > 0) or (java_version != ''):
            java_version = '.' + java_version_update + java_version
        if (int(java_version_interim) > 0) or (java_version != ''):
            java_version = '.' + java_version_interim + java_version
        java_version = java_version_feature + java_version
        java_version_short = java_version
    else:
        java_version_major = java_version_parts[1]
        java_version_minor = java_version_parts[2].split('_')[1]
        java_version_short = java_version_major + 'u' + java_version_minor
    path_separator = '/'
    temp_dir = '/tmp'

    os = host.system_info.distribution
    if os.lower() in ['ubuntu', 'debian']:
        java_installer_ext = '.tar.gz'
        platform = 'linux'
    elif os.lower() in ['centos', 'rhel']:
        java_installer_ext = '.rpm'
        platform = 'linux'
    elif os == 'Mac OS X':
        java_installer_ext = '.dmg'
        if int(java_version_parts[0]) > 8:
            platform = 'osx'
        else:
            platform = 'macosx'
    elif os == 'Windows':
        java_installer_ext = '.exe'
        platform = 'windows'
        path_separator = '\\'
        temp_dir = 'C:\\Program Files\\Ansible\\temp'
    else:
        java_installer_ext = 'need-ext-for-' + os
        platform = os

    if int(java_version_parts[0]) > 8:
        java_installer_filename = (
            'jdk-' + java_version + '_' + platform + '-x64_bin' + java_installer_ext
        )
    else:
        java_installer_filename = (
            'jdk-' + java_version_short + '-' + platform + '-x64' + java_installer_ext
        )

    test_vars = {
        'java_version': java_version,
        'java_version_short': java_version_short,
        'java_installer_filename': java_installer_filename,
        'temp_dir': temp_dir,
        'path_separator': path_separator
    }
    return test_vars


def test_java_version_fact(host, test_vars):
    f = host.file(test_vars['temp_dir'] +
                  test_vars['path_separator'] + 'vars_log.txt')
    java_version_string = 'java_version=' + test_vars['java_version']
    assert f.exists
    assert f.contains(java_version_string)


def test_java_installer_filename_fact(host, test_vars):
    f = host.file(test_vars['temp_dir'] +
                  test_vars['path_separator'] + 'vars_log.txt')
    java_installer_filename_string = 'java_installer_filename=' + \
        test_vars['java_installer_filename']
    assert f.exists
    assert f.contains(java_installer_filename_string)


def test_installer_exists(host, test_vars):
    installer_filepath = test_vars['temp_dir'] + \
        test_vars['path_separator'] + test_vars['java_installer_filename']
    f = host.file(installer_filepath)
    assert f.exists


def test_java_version_installed(host, test_vars):
    result = host.run("java -version")
    assert test_vars['java_version'] in result.stderr


def test_java_crypto_enabled(host):
    result = host.run(
        "jrunscript -e 'exit (javax.crypto.Cipher.getMaxAllowedKeyLength(\"RC5\") >= 256);'")
    assert result.rc == 1
