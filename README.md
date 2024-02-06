# MySQL Dynamic Inventory Plugin for Ansible

## Overview

This Ansible inventory plugin, named `mysql-dynamic-inventory`, allows you to dynamically generate your Ansible inventory by executing a custom SQL query against a MySQL database.

## Features

- **Dynamic Inventory Generation:** Fetch hosts dynamically from a MySQL database based on a custom SQL query.
- **Custom Host Variables:** Automatically assign any column returned by the query as Ansible host variables.

## Requirements

- Ansible 2.9 or later.
- PyMySQL 0.9.3 or later (or adjust according to your compatibility).

## Installation

Place the `mysql-dynamic-inventory.py` file in your Ansible inventory directory or in a custom directory that Ansible is configured to search for inventory plugins.

## Configuration

1. **Plugin Configuration File:** Create a YAML configuration file (e.g., `my-dynamic-inventory-mysql.yml` - must end with mysql.yml/yaml) with the necessary database connection details and your SQL query. Here is a template:

```yaml
plugin: mysql-dynamic-inventory
db_host: mysql_server
db_user: mysql_user
db_pass: mysql_pass
db_name: mysql_database
db_query: |
  SELECT 'some_inventory_hostname' as inventory_hostname,
         'some_inventory_group' as inventory_group,
         'some_ansible_host' as ansible_host,
         'somerandomvar' as coolrandomvar
```

2. **Required Columns:** Ensure your SQL query provides at least the `inventory_group` and `inventory_hostname` columns. Additional columns will be dynamically added as host variables.

## Usage

To use the plugin, simply point Ansible to your `my-dynamic-inventory-mysql.yml` file when running commands or playbooks:

```bash
ansible-inventory -i my-dynamic-inventory-mysql.yml --graph
ansible-playbook -i my-dynamic-inventory-mysql.yml your_playbook.yml
```

## Troubleshooting

If you encounter errors, ensure:
- Your MySQL server is accessible from the host running Ansible.
- Your SQL query is correctly formatted and returns the required columns.
- You have installed the necessary Python dependencies.

## Contributing

Contributions to improve `mysql-dynamic-inventory` are welcome. Please ensure to follow best practices and open a pull request for any enhancements.


## Acknowledgments

A humble thank you to all contributors and users of this plugin for your support and feedback.
