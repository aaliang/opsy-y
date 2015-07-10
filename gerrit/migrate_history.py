#!/usr/bin/env python

#half written script to load info from dumped files (dump_history) into a new gerrit sql instance.
#half written because its not genericizable

import os
import json

PATH_TO_NEW_GERRIT_DIR = '../../gerrit2/'
PATH_TO_NEW_GERRIT_WAR = '../../gerrit2/bin/gerrit.war'
#technically it can be any gerrit.war

DUMP_BASE_COMMAND = 'java -jar ' + PATH_TO_GERRIT_WAR + ' gsql -c "%(sql_command)s -d ' + PATH_TO_NEW_GERRIT_DIR

TABLES_TO_LOAD = [
  'ACCOUNT_PATCH_REVIEWS',
  'CHANGE_MESSAGES',
  'CHANGES',
  'PATCH_COMMENTS',
  'PATCH_SET_ANCESTORS',
  'PATCH_SET_APPROVALS',
  'PATCH_SETS'
]

INSERT_PREFIX = 'INSERT INTO %(table_name) (%(columns)s)'

for table_name in TABLES_TO_LOAD:
  file = open(table_name, 'r')
  #get the first line to get the schema
  schema = [x.lower() for x in file.readline().split(',')]

  INSERT_INTO = INSERT_PREFIX % {'table_name': table_name, 'columns': ",".join(schema)}

  for row_str in file:
    row = json.loads(row_str)
    if 'columns' in row:
      columns = row['columns']
