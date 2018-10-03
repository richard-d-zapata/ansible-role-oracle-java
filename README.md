# Oracle Java

Install Oracle Java (JDK)

## Requirements

None

## Environment Variables

| Option                       | Default | Example                               |
| :--------------------------- | :------ | :------------------------------------ |
| `JAVA_LINUX_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Linux/Java` |
| `JAVA_MACOS_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/macOS/Java` |
| `JAVA_INSTALLERS_PATH`       | none    | `/Users/Shared/Installers/Java`       |

## Role Variables

| Option                 | Default                    | Example                         |
| :--------------------- | :------------------------- | :------------------------------ |
| `java_version`         | `11`                       | `10.0.2`                        |
| `java_installers_path` | `/Users/Shared/Installers` | `/Users/Shared/Installers/Java` |

## Dependencies

None

## Example Playbook

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - name: Install Oracle JDK 11
      hosts: servers
      roles:
         - { role: kaos2oak.oracle-java }

## Role Testing

You will need to install molecule first:

    pip install molecule
    pip install docker-py

To run the tests:

    molecule test

## License

MIT

## Author Information

Justin Sako
