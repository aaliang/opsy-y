#copies the git and h2 files from remote onto your local directory

#USER@DOMAIN for ssh
REMOTE="ec2-user@mydomain.com"

#assuming that permissions are in a pem file
PATH_TO_PEM_FILE="$HOME/.ssh/my-pem.pem";

rsync -rave "ssh -i $PATH_TO_PEM_FILE" $REMOTE:/opt/gerrit/db/  ~/gerrit/db/

#just use rsync to copy over. could probably git pull it too. but your old instance
#is probably down :)
rsync -rave "ssh -i $PATH_TO_PEM_FILE" $REMOTE:/opt/gerrit/git/  ~/gerrit/git/
