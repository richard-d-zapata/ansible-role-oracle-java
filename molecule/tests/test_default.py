import os
import pytest
import testinfra.utils.ansible_runner
import pprint

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture(scope='module')
def test_vars(host):
    java_version_feature = 11
    java_version_interim = 0
    java_version_update = 0
    java_version_patch = 0
    java_version = ''
    if java_version_patch > 0:
        java_version = '.' + str(java_version_patch)
    if java_version_update > 0:
        java_version = '.' + str(java_version_update) + java_version
    if java_version_interim > 0:
        java_version = '.' + str(java_version_interim) + java_version
    java_version = str(java_version_feature) + java_version
    java_version_short = java_version
    path_separator = '/'
    temp_dir = '/tmp'

    os = host.system_info.distribution
    if os.lower() == 'ubuntu':
        java_installer_ext = '.tar.gz'
        platform = 'linux'
    elif os.lower() == 'centos':
        java_installer_ext = '.rpm'
        platform = 'linux'
    elif os == 'Mac OS X':
        java_installer_ext = '.dmg'
        platform = 'macosx'
    elif os == 'Windows':
        java_installer_ext = '.exe'
        platform = 'windows'
        path_separator = '\\'
        temp_dir = 'C:\\Program Files\\Ansible\\temp'
    else:
        java_installer_ext = os
        platform = os

    java_installer_filename = (
        'jdk-' + java_version + '_' + platform + '-x64_bin' + java_installer_ext
    )

    test_vars = {
        'java_version'            : java_version,
        'java_version_short'      : java_version_short,
        'java_installer_filename' : java_installer_filename,
        'temp_dir'                : temp_dir,
        'path_separator'          : path_separator
    }
    return test_vars

def test_java_version_fact(host, test_vars):
    f = host.file(test_vars['temp_dir'] + test_vars['path_separator'] + 'vars_log.txt')
    java_version_string = 'java_version=' + test_vars['java_version']
    assert f.exists
    assert f.contains(java_version_string)


def test_java_installer_filename_fact(host, test_vars):
    f = host.file(test_vars['temp_dir'] + test_vars['path_separator'] + 'vars_log.txt')
    java_installer_filename_string = 'java_installer_filename=' + test_vars['java_installer_filename']
    assert f.exists
    assert f.contains(java_installer_filename_string)


def test_installer_exists(host, test_vars):
    installer_filepath = test_vars['temp_dir'] + test_vars['path_separator'] + test_vars['java_installer_filename']
    f = host.file(installer_filepath)
    assert f.exists


def test_java_version_installed(host, test_vars):
    result = host.run("java -version")
    assert test_vars['java_version'] in result.stderr


# @pytest.fixture(scope='module')
# def test_vars(host):
#     java_version_feature = 11
#     java_version_interim = 0
#     java_version_update = 0
#     java_version_patch = 0
#     if java_version_feature > 8:
#         java_version = ''
#         if java_version_patch > 0:
#             java_version = '.' + java_version_patch
#         if java_version_update > 0:
#             java_version = '.' + java_version_update + java_version
#         if java_version_interim > 0:
#             java_version = '.' + java_version_interim + java_version
#         java_version = java_version_feature + java_version
#         java_version_short = java_version
#     else:
#         java_version = '1.' + java_version_feature + '.0_' + java_version_interim
#         java_version_short = java_version_feature + 'u' + java_version_interim
#     path_separator = '/'
#     temp_dir = '/tmp'

#     os = host.system_info.distribution
#     if os == 'ubuntu':
#         java_installer_ext = '.tar.gz'
#         platform = 'linux'
#     elif os == 'centos':
#         java_installer_ext = '.rpm'
#         platform = 'linux'
#     elif os == 'Mac OS X':
#         java_installer_ext = '.dmg'
#         platform = 'macosx'
#     elif os == 'Windows':
#         java_installer_ext = '.exe'
#         platform = 'windows'
#         path_separator = '\\'
#         temp_dir = 'C:\\Program Files\\Ansible\\temp'
#     else:
#         java_installer_ext = os

#     if java_version_feature > 8:
#         java_installer_filename = (
#             'jdk-' + java_version + '_' + platform + '-x64_bin' + java_installer_ext
#         )
#     else:
#         java_installer_filename = (
#             'jdk-' + java_version_short + '-' + platform + '-x64' + java_installer_ext
#         )

#     test_vars = {
#         'java_version_major'      : java_version_major,
#         'java_version_minor'      : java_version_minor,
#         'java_version'            : java_version,
#         'java_version_short'      : java_version_short,
#         'java_installer_filename' : java_installer_filename,
#         'temp_dir'                : temp_dir,
#         'path_separator'          : path_separator
#     }
#     return test_vars
