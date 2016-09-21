Installion
---
1. Install Vagrant and Virtual Box
	Follow directions here: https://udacity.atlassian.net/wiki/display/BENDH/Vagrant+VM+Installation
	Clone this fullstack-nanodegree-vm instead of one refered to there.

Running
---
1. On the vagrant VM go to /vagrant/tournament
2. Create "tournament" database:
	vagrant => CREATE DATABASE tournament;
3. Load tournament.sql
	vagrant@trusty32: psql => \i tournament.sql
4. Run python script:
	python tournament_test.sql
