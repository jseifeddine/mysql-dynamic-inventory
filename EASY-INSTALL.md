Copy the `mysql-dynamic-inventory.py` file to your inventory plugins dir...

The inventory plugin path can be found by running the command:

`ansible-config dump | grep INVENTORY_PLUGIN`

Example output:

`DEFAULT_INVENTORY_PLUGIN_PATH(/etc/ansible/ansible.cfg) = ['/etc/ansible/plugins/inventory']`

As you can see from the Example output above, my inventory plugin path is `/etc/ansible/plugins/inventory` - so copy the file into that directory, or like i have (for organization), a sub directory called `mysql-dynamic-inventory`

So in the example case, the file should live at:

`/etc/ansible/plugins/inventory/mysql-dynamic-inventory/mysql-dynamic-inventory.py`

Then in your inventory YAML file, specify the plugin, db connections details, and query... as so.

web-servers-mysql.yml:
```yaml
#   Required columns: 
#   'inventory_group', 'inventory_hostname'
#
#   TLDR:
#   Besides the required columns, each column will be assigned 
#   as an ansible hostvar dynamically.

plugin: mysql-dynamic-inventory
db_host: mysql_server
db_user: mysql_user
db_pass: mysql_pass
db_name: mysql_database
db_query: |
  SELECT ip_address as ansible_host, hostname as inventory_hostname, 'web_servers' as inventory_group from servers where hostname like "web%";
```


Then verify the inventory with:

`ansible-inventory -i web-servers-mysql.yml --graph`

or

`ansible-inventory -i web-servers-mysql.yml --list`
