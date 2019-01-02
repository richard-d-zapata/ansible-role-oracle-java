# Kaos2oak Oracle Java

Install Oracle Java (JDK)

This role is designed to install Java JDK. The role should work with Java
versions 7 and higher, but has not been extensively tested on all possible
major and minor versions.

## Goal

The initial goal for this role is to provide a method to provision macOS,
Ubuntu, RedHat and Windows with Oracle Java using the same role, so that
a single playbook may be used to provision all of these platforms for
software testing.

Important considerations before using this role:

- no attempt to provide the security that would be necessary for a production
  installation has been included
- the role is designed to be able to specify particular versions to be
  installed, rather than simply "the latest"

## Requirements

This role is designed to be used with a Java installer downloaded from Oracle
and placed locally on your "controller" (the machine from which you are running
the Ansible playbook). Oracle has made it difficult to download any installers
that are not the latest version available. If you want to use this role and
have the installer automatically downloaded from Oracle (which will only work
with latest installers), you may need to do the following (using information
from the Oracle website for reference) if the `main.yml` defaults file
doesn't already contain the latest version information:

- Provide the latest Java version
- Provide the download path for the latest Java installers

To do so, navigate to the Oracle [Java SE](https://www.oracle.com/technetwork/java/javase/overview/index.html)
download page, go to the latest version page, accept the license agreement and
copy the link for one of the installer downloads. You can now use this link
minus the name of the installer as the `java_installer_url_path` in the playbook
or `JAVA_INSTALLER_URL_PATH` environment variable.

If you are running Ansible 2.4 or above on macOS High Sierra or above, you may
want to learn more about an issue with "changes made in High Sierra that are
breaking lots of Python things that use fork()."
See Ansible issue [32499](https://github.com/ansible/ansible/issues/32499) for
more information.

Because of the above issue, you may want to include this line in your
`Vagrantfile` if you are using vagrant:

    ENV["VAGRANT_OLD_ENV_OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

Or, export this information before executing the role:

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

_Note: The provisioning of a Windows VM seems to be particularly sensitive to_
_this._

## Environment Variables

Variables that are particular to the environment from which you are running
the playbook can be supplied as environment variables so that they can be
"sourced" from a file in the environment.  This provides an easy way to
supply different paths to resources if you are using the roles on different
computers.

| Option                               | Default | Example                                                                                  |
| :----------------------------------- | :------ | :--------------------------------------------------------------------------------------- |
| `JAVA_VERSION`                       | none    | `10.0.2` or `1.8.0_192`                                                                  |
| `JAVA_LINUX_LOCAL_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/Linux/Java`                                                    |
| `JAVA_MAC_LOCAL_INSTALLERS_PATH`     | none    | `/Users/Shared/Installers/macOS/Java`                                                    |
| `JAVA_WINDOWS_LOCAL_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Windows/Java`                                                  |
| `LINUX_LOCAL_INSTALLERS_PATH`        | none    | `/Users/Shared/Installers/Linux`                                                         |
| `MAC_LOCAL_INSTALLERS_PATH`          | none    | `/Users/Shared/Installers/macOS`                                                         |
| `WINDOWS_LOCAL_INSTALLERS_PATH`      | none    | `/Users/Shared/Installers/Windows`                                                       |
| `JAVA_LOCAL_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/Java`                                                          |
| `LOCAL_INSTALLERS_PATH`              | none    | `/Users/Shared/Installers`                                                               |
| `JAVA_INSTALLER_URL_PATH`            | none    | `http://download.oracle.com/otn-pub/java/jdk/11.0.1+13/90cf5d8f270a4347a95050320eef3fb7` |

_Note: One or more of the `INSTALLERS_PATH` environment variables may be_
_defined and the role will search the paths in the above order until it_
_finds an installer. If it does not find an installer locally, it will_
_attempt to download the installer, but this is only likely to work for_
_the latest installer versions, due to download restrictions that Oracle_
_has in place._

## Role Variables

Variables that are targeted toward options to use during the execution of the
roles are left to be specified as role variables and can be specified in the
playbook itself or on the command line when running the playbook.

| Option                      | Default                      | Example                                                                                  |
| :-------------------------- | :--------------------------- | :--------------------------------------------------------------------------------------- |
| `java_version`              | `11.0.1`                     | `10.0.2` or `1.8.0_192`                                                                  |
| `java_installers_path_list` | [`/Users/Shared/Installers`] | [`/Users/Shared/Installers`,`/Users/myaccount/Desktop`]                                  |
| `java_installer_url_path`   | see `main.yml` in `defaults` | `http://download.oracle.com/otn-pub/java/jdk/11.0.1+13/90cf5d8f270a4347a95050320eef3fb7` |

_Note: Using `java_installers_path_list` or `java_installer_url_path` might_
_not be considered "normal usage", but is supported for use in playbooks or_
_other scenarios in which it makes sense._

_Note: Using `java_installers_path` is still supported, but is deprecated_
_and will be removed with the next breaking change._

## Dependencies

If you wish to install an older version of Java with the JCE on RedHat, you
will need to make sure RedHat is registered with a repository where `unzip`
is available for installation.

## Role Use

Use of this role consists of the following:

- Create a playbook
- Obtain and have the desired installer available locally on the ansible
  controller
- Provide the location of the installer on the controller as an environment
  variable, in the playbook or as an extra-var
- Provide the version of Java (must match the installer) as an environment
  variable, in the playbook or as an extra-var
- Run the playbook

### Example Playbooks

``` yaml
- name: Install default Oracle JDK
    hosts: servers
    roles:
        - { role: kaos2oak.oracle-java }
```

_Note: See the `defaults.yml` file for the "default" Java version that will_
_be installed by the above playbook._

``` yaml
- name: Install Oracle JDK 11.0.1
    hosts: servers
    vars:
        java_version: '11.0.1'
    roles:
        - { role: kaos2oak.oracle-java }
```

``` yaml
- name: Install Oracle JDK 8u192
    hosts: servers
    vars:
        java_version: '1.8.0_192'
    roles:
        - { role: kaos2oak.oracle-java }
```

``` yaml
- name: Install Oracle JDK 7u80 with JCE
    hosts: servers
    vars:
        java_version: '1.7.0_80'
    roles:
        - { role: kaos2oak.oracle-java }
```

### Example Installer Locations

If you really want it to be quick and easy:

    export LOCAL_INSTALLERS_PATH="$HOME/Downloads"

Or, you could always move the installers to a more permanent default location
after downloading them and then point to that location:

    export JAVA_LOCAL_INSTALLERS_PATH="/Users/Shared/Installers/Java"

If you like to keep things neat and organized, you might organize the installers
into folders, create a file named something like `setup` in a directory named
`my` in this repository (most contents of the `my` directory are part of the
.gitignore ignored files, so it will not be part of any commit) and then
`source` the file:

``` shell
# File: setup
export JAVA_MAC_LOCAL_INSTALLERS_PATH="$HOME/Installers/Mac/Java"
export JAVA_LINUX_LOCAL_INSTALLERS_PATH="$HOME/Installers/Linux/Java"
export JAVA_WINDOWS_LOCAL_INSTALLERS_PATH="$HOME/Installers/Windows/Java"
```

    source my/setup

### Example Java Version

Since the Java version may be something that you want to change on the fly,
you probably don't want to include it in the `setup` file, but you can always
provide it on the command line before the ansible-playbook run:

    export JAVA_VERSION=1.8.0_192

Or, provide it as an "extra-vars" role variable for the ansible-playbook run:

    -e "java_version=11.0.1"

### Example Playbook Runs

Assuming you have created a playbook named `k2o-java.yml`:

    ansible-playbook k2o-java.yml

    JAVA_VERSION=1.8.0_152 ansible-playbook k2o-java.yml

    ansible-playbook k2o-java.yml -e "java_version=1.8.0_152"

If the playbook itself contains the version of Java, it might look like:

    ansible-playbook k2o-java-7u80.yml

## Role Testing

### Pre-requisites

[Molecule](https://molecule.readthedocs.io/en/latest/) is being used for
testing this role.

_Note: Windows testing with Molecule is not actively supported, so these tests_
_may not work._

You will need to install molecule and python support modules before running
the role tests:

    pip install molecule
    pip install docker-py

You also need to install the following before running the vagrant role tests:

    pip install python-vagrant

You may also need to run the following command prior to executing molecule
tests with vagrant (see [Requirements](#requirements)):

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

The 'verifier' for Windows is disabled as I have not yet been able to get the
testinfra verfication to work for Windows. If you have any experience or advice
in this area, please let me know.

### Java Versions in Molecule tests

To run the molecule tests for a particular Java version, you will need to
provide the `JAVA_VERSION` as an environment variable and ensure the installer
is located locally in the appropriate ...`INSTALLERS_PATH` location. See
examples, below.

It is also possible to edit the `molecule.yml` file for a scenario and
specify the java_version like this:

    provisioner:
      name: ansible
      env:
        JAVA_VERSION: 1.8.0_192

### Default Tests

Ubuntu 18, CentOS 7 via docker:

    molecule test

or

    JAVA_VERSION=1.8.0_192 molecule test

### Ubuntu Tests

Ubuntu 18, 16, 14, 12 via docker:

    molecule test --scenario-name ubuntu-docker

Ubuntu 18 via vagrant:

    molecule test --scenario-name ubuntu-vagrant

### CentOS/RedHat Tests

CentOS 7, 6 via docker:

    molecule test --scenario-name centos-docker

### macOS Tests

macOS 10.13, 10.12, 10.11 via vagrant:

    molecule test --scenario-name macos-vagrant

### Windows Tests

Window 2012r2 via vagrant (may not work):

    molecule test --scenario-name windows-vagrant

## Docker Space Issues

If you find that your drive space is disappearing, you may want to refer to
[Docker for Mac: reducing disk space](https://djs55.github.io/jekyll/update/2017/11/27/docker-for-mac-disk-space.html).

## License

MIT

## Author Information

Justin Sako
