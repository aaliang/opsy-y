#!/usr/bin/env python

#place this in your local dev root folder
#so, for example if all my gerrit repos were in /home/aliang/dev/ this would be /home/aliang/dev/migrate.py
#from that directory run: $ pythor remote-batch-migrate.py

#you should then be good to go. can validate by checking the contents of each .gitreview file or
#run git remote -v

import os, ConfigParser

#add repos here
repos = [
  'engine',
  'repo1',
  'repo2',
  'repo3'
]

username = 'Andy'

_git = 'git --git-dir %(repo_name)s/.git'
#your host
host = 'my.gitrepo.com'

#assumed to be a gerrit install, hence the 29418 port
add_new_remote = _git + ' remote add %(remote_name)s ssh://%(username)s@%(host)s:29418/%(repo_name)s.git'
rmv_old_remote = _git + ' remote rm %(remote_name)s'

for repo in repos:
  for remote_name in ['gerrit', 'origin']:
    rmv_command = rmv_old_remote % {'remote_name': remote_name, 'repo_name': repo}
    add_command = add_new_remote % {'remote_name': remote_name, 'username': username, 'repo_name': repo, 'host': host}

    os.system(rmv_command)
    os.system(add_command)

    try:
      config = ConfigParser.RawConfigParser()
      config.read(repo + '/.gitreview')
      config.set('gerrit', 'host', host)

      with open(repo + '/.gitreview', 'wb') as configfile:
        config.write(configfile)

    except:
      pass
