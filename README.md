# Oracle Java

Install Oracle Java (JDK)

This role is designed to install Java 11.  It may install version 10, but has
not been tested.  It is not designed for versions below 10 and Oracle's new
Java naming scheme.

## Requirements

Currently, this role requires you to download the Java installer from Oracle
and have it placed locally on your "controller" (the machine from which you
are running the Ansible playbook).

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

| Option                         | Default | Example                                 |
| :----------------------------- | :------ | :-------------------------------------- |
| `JAVA_LINUX_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/Linux/Java`   |
| `JAVA_MACOS_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/macOS/Java`   |
| `JAVA_WINDOWS_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Windows/Java` |
| `JAVA_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/Java`         |

## Role Variables

| Option                 | Default                    | Example                         |
| :--------------------- | :------------------------- | :------------------------------ |
| `java_version`         | `11`                       | `10.0.2`                        |
| `java_installers_path` | `/Users/Shared/Installers` | `/Users/Shared/Installers/Java` |

## Dependencies

None

## Example Playbook

    - name: Install Oracle JDK 11
      hosts: servers
      roles:
         - { role: kaos2oak.oracle-java }

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

### Default Tests

Ubuntu 18, CentOS 7 via docker:

    molecule test

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
