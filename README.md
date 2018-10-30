# Oracle Java

Install Oracle Java (JDK)

This role is designed to install Java JDK. The role should work with Java
versions 7 and higher, but has not been extensively tested on all possible
minor versions.

## Requirements

This role is designed to be used with a Java installer downloaded from Oracle
and placed locally on your "controller" (the machine from which you are running
the Ansible playbook). Oracle has made it difficult to download any installers
that are not the latest version available. If you want to use this role and
have the installer automatically downloaded from Oracle (which will only work
with latest installers), you may need to do the following (using information
from the Oracle website for reference) if the `main.yml` defaults file
doesn't already contain the latest version information:

* Provide the latest Java version
* Provide the download path for the latest Java installers

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

You may also need to run the following command prior to executing molecule
tests with vagrant:

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

## Environment Variables

| Option                         | Default | Example                                                                                  |
| :----------------------------- | :------ | :--------------------------------------------------------------------------------------- |
| `JAVA_LINUX_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/Linux/Java`                                                    |
| `JAVA_MACOS_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/macOS/Java`                                                    |
| `JAVA_WINDOWS_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Windows/Java`                                                  |
| `JAVA_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/Java`                                                          |
| `JAVA_VERSION`                 | none    | `10.0.2` or `1.8.0_192`                                                                  |
| `JAVA_INSTALLER_URL_PATH`      | none    | `http://download.oracle.com/otn-pub/java/jdk/11.0.1+13/90cf5d8f270a4347a95050320eef3fb7` |

## Role Variables

| Option                    | Default                    | Example                                                                                  |
| :------------------------ | :------------------------- | :--------------------------------------------------------------------------------------- |
| `java_version`            | `11.0.1`                   | `10.0.2` or `1.8.0_192`                                                                  |
| `java_installers_path`    | `/Users/Shared/Installers` | `/Users/Shared/Installers/Java`                                                          |
| `java_installer_url_path` | current URL                | `http://download.oracle.com/otn-pub/java/jdk/11.0.1+13/90cf5d8f270a4347a95050320eef3fb7` |

## Dependencies

None

## Role Use

Use of this role consists of the following:

* Create a playbook
* Obtain and have the desired installer available locally on the ansible
  controller
* Provide the location of the installer on the controller as an environment
  variable, in the playbook or as an extra-var
* Provide the version of Java (must match the installer) as an environment
  variable, in the playbook or as an extra-var
* Run the playbook

### Example Playbooks

``` yaml
- name: Install Oracle JDK
    hosts: servers
    roles:
        - { role: kaos2oak.oracle-java }
```

``` yaml
- name: Install Oracle JDK 8u192
    hosts: servers
    vars:
        java_version: 1.8.0_192
    roles:
        - { role: kaos2oak.oracle-java }
```

``` yaml
- name: Install Oracle JDK 7u80 with JCE
    hosts: servers
    vars:
        java_version: 1.7.0_80
    roles:
        - { role: kaos2oak.oracle-java }
```

### Example Installer Locations

If you really want it to be quick and easy:

    export JAVA_INSTALLERS_PATH="$HOME/Downloads"

Or, you could always move the installers to the default location after
downloading them:

    /Users/Shared/Installers/Java

If you like to keep things neat and organized, you might organize the installers
into folders, create a file named something like `setup` in a directory named
`my` in this repository (the `my` directory is part of the .gitignore, so it
will not be part of any commit) and then `source` the file:

``` shell
# File: setup
export JAVA_MACOS_INSTALLERS_PATH="$HOME/Installers/Mac/Java"
export JAVA_LINUX_INSTALLERS_PATH="$HOME/Installers/Linux/Java"
export JAVA_WINDOWS_INSTALLERS_PATH="$HOME/Installers/Windows/Java"
```

    source my/setup

### Example Java Version

Since the Java version may be something that you want to change on the fly,
you probably don't want to include it in the `setup` file, but you can always
provide it on the command line before the ansible-playbook run:

    export JAVA_VERSION=1.8.0_192

Or, provide as part of the ansible-playbook run (see below).

### Example Playbook Runs

Assuming you have created a playbook named `k2o-java.yml`:

    ansible-playbook k2o-java.yml

    JAVA_VERSION=1.8.0_152 ansible-playbook k2o-java.yml

    ansible-playbook k2o-java.yml -e "java_version=1.8.0_152"

If the playbook itself contains the version of Java:

    ansible-playbook k2o-java-7u80.yml

## Role Testing

### Pre-requisites

[Molecule](https://molecule.readthedocs.io/en/latest/) is being used for
testing this role.

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

### Java Versions

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

Window 2012r2 via vagrant:

    molecule test --scenario-name windows-vagrant

## Docker Space Issues

If you find that your drive space is disappearing, you may want to refer to
[Docker for Mac: reducing disk space](https://djs55.github.io/jekyll/update/2017/11/27/docker-for-mac-disk-space.html).

## License

MIT

## Author Information

Justin Sako
