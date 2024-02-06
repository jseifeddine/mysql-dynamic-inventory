#!/usr/bin/env python3

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError
import pymysql

DOCUMENTATION = r'''
    name: mysql-dynamic-inventory
    plugin_type: inventory
    short_description: Returns Ansible inventory from an SQL query
    description: Returns Ansible inventory from an SQL query
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['mysql-dynamic-inventory']
      db_host:
        description: Database host
        required: true
      db_user:
        description: Database user
        required: true
      db_pass:
        description: Database password
        required: true
      db_name:
        description: Database name
        required: true
      db_query:
        description: Database query
        required: true
'''

class InventoryModule(BaseInventoryPlugin):

    NAME = 'mysql-dynamic-inventory'

    def verify_file(self, path):
        '''Ensures that the given file is valid for this plugin'''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('mysql.yaml',
                              'mysql.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        '''Parses the inventory file'''
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        self._fetch_hosts()

    def _fetch_hosts(self):
        '''Fetches hosts from the database and populates the inventory'''
        group_init = {}
        try:
            connection = pymysql.connect(host=self.get_option('db_host'),
                                        user=self.get_option('db_user'),
                                        password=self.get_option('db_pass'),
                                        database=self.get_option('db_name'),
                                        cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute(self.get_option('db_query'))
                for row in cursor.fetchall():
                    group = row.get('inventory_group')
                    if group and group not in group_init:
                        self.inventory.add_group(group)
                        group_init[group] = True
                    hostname = row.get('inventory_hostname')
                    if hostname:
                        self.inventory.add_host(hostname, group=group)
                        # Dynamically set ansible host variables for each column returned
                        for key, value in row.items():
                            # Skip inventory_hostname and group as they're already used
                            if key not in ['inventory_hostname', 'inventory_group']:
                                self.inventory.set_variable(hostname, key, value)
        except Exception as e:
            raise AnsibleError(f"Database query failed: {e}")
        finally:
            if connection:
                connection.close()

