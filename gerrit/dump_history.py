#!/usr/bin/env python

#dumps all history from tables gerrit's shitty sql impl into a bunch of json files
#we are scripting against the java command gsql

import os
import json

#for now make the following assumptions
PATH_TO_GERRIT_DIR = '..'
PATH_TO_GERRIT_WAR = './gerrit.war'

BASE_COMMAND_JSON = 'java -jar ' + PATH_TO_GERRIT_WAR + ' gsql -c "%(sql_command)s" --format JSON -d ' + PATH_TO_GERRIT_DIR
LIST_TABLES = BASE_COMMAND_JSON % {'sql_command': 'SHOW TABLES;'}

to_import = filter(
  lambda x: x['type'] == 'row',
  map(json.loads, os.popen(LIST_TABLES))
)

#for each table, write out each row as json into file
for table in to_import:
  table_name = table['columns']['table_name']

  args = {'table_name': table_name }

  schema_list = os.popen(BASE_COMMAND_JSON % {'sql_command': 'SHOW COLUMNS FROM %(table_name)s;' % args})

  schema = [field['columns']['field'] for field in map(json.loads, schema_list) if field['type'] == 'row']

  file = open(table_name, 'w')

  file.write(','.join(schema))
  file.write('\n')

  for line in os.popen(BASE_COMMAND_JSON % {'sql_command': 'SELECT * FROM %(table_name)s' % args}):
    file.write(line)
