# Oracle Java

Install Oracle Java (JDK)

## Requirements

None

## Role Variables

| Option                | Default | Example  |
| :-------------------- | :------ | :------- |
| `java_version_string` | `11`    | `10.0.2` |

## Dependencies

None

## Example Playbook

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - name: Install Oracle JDK 11
      hosts: servers
      roles:
         - { role: k2o.oracle-java }

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
