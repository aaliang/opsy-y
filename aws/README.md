remove-stale-ami.js

aws utility to remove stale AMIs (should probably live outside of this repo) usage: node remove-stale-ami.js {MIN_AMIS} {MAX_AMIS} {CUTOFF_DAYS}

removes ami's that are have been created more than {CUTOFF_DAYS} days ago,
for the ami's that are have been around for less than {CUTOFF_DAYS} days, keeps only the {MAX_AMIS} most recent
keeps at a minimum {MIN_AMIS} images (unless there are less images to begin with)
