#!/usr/bin/env python

#half written script to load info from dumped files (dump_history) into a new gerrit sql instance.
#half written because its not genericizable
#as such, this is not intended to do the work but rather to build a springboard over which we can
#either interactively script over, or customize as we see fit

#we can't just copy over the h2 files because OpenIds change per host
#this has the effect of essentially invalidating all admin rights, even if the user is marked as an admin
#therefore, we need to copy over the relevant review information from old gerrit to new gerrit
#many things to consider here. such as user id etc

import os
import json

#these paths are assumed, should actually use cmdlineargs but not going to do that
PATH_TO_NEW_GERRIT_DIR = '../../gerrit2/'
PATH_TO_NEW_GERRIT_WAR = '../../gerrit2/bin/gerrit.war'
#technically it can be any gerrit.war

DUMP_BASE_COMMAND = 'java -jar ' + PATH_TO_GERRIT_WAR + ' gsql -c "%(sql_command)s -d ' + PATH_TO_NEW_GERRIT_DIR

#we're really only interested in moving these tables over
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
      #have to map over user ids
