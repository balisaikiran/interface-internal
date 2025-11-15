#!/bin/bash

echo $STAGE
date >> ~/last_deploy.txt
if [[ $STAGE == "prod" ]]; then
        cd /var/www/front-end/
        echo Production Mode
        echo Pulling from Bitbucket
        sudo git stash
        sudo git checkout master
        sudo git pull origin
        echo Permissions Updated
        sudo chown www-data:www-data /var/www/front-end/sharpdata
        sudo chown www-data:www-data /var/www/front-end/sharpdata/db.sqlite3
        sudo chmod 664 /var/www/front-end/sharpdata/db.sqlite3
        echo Database Permissions Updated
        echo Installing Dependencies
        source ~/venv/bin/activate
        pip install -r /var/www/front-end/sharpdata/requirement.txt 
        echo Restarting Apache2 server
        sudo service apache2 restart
        # curl -X POST -H 'Content-type: application/json' --data '{"text":"Deployed to Prod"}' https://hooks.slack.com/services/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
        curl -X POST --data-urlencode "payload={\"channel\": \"#datalabz-dev-sprint-deployment\", \"username\": \"EC2_Deployment_Alert\", \"text\": \"Deployed to Prod\"}" https://hooks.slack.com/services/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
fi
if [[ $STAGE == "test" ]]; then
        cd /var/www/front-end/
        echo Production Mode
        echo Pulling from Bitbucket
        sudo git stash
        sudo git checkout staging
        sudo git pull origin
        echo Permissions Updated
        sudo chown www-data:www-data /var/www/front-end/sharpdata
        sudo chown www-data:www-data /var/www/front-end/sharpdata/db.sqlite3
        sudo chmod 664 /var/www/front-end/sharpdata/db.sqlite3
        echo Database Permissions Updated
        echo Installing Dependencies
        source ~/venv/bin/activate
        pip install -r /var/www/front-end/sharpdata/requirement.txt 
        echo Restarting Apache2 server
        sudo service apache2 restart
        curl -X POST -H 'Content-type: application/json' --data '{"text":"Deployed to Test"}' https://hooks.slack.com/services/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
fi
if [[ $STAGE == "dev" ]]; then
        cd /var/www/sharpdata/front-end/
        echo Development Mode
        echo Pulling from Bitbucket
        sudo git stash
        sudo git checkout develop
        sudo git pull origin
        echo Permissions Updated
        sudo chown :www-data sharpdata/db.sqlite3 
        sudo chmod 664 sharpdata/db.sqlite3
        echo Database Permissions Updated
        echo Installing Dependencies
        source ~/venv/bin/activate
        pip install -r /var/www/front-end/sharpdata/requirement.txt 
        echo Restarting Apache2 server
        sudo service apache2 restart
        curl -X POST --data-urlencode "payload={\"channel\": \"#datalabz-dev-sprint-deployment\", \"username\": \"EC2_Deployment_Alert\", \"text\": \"Deployed to Develop\"}" https://hooks.slack.com/services/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
fi
if [[ -z "$STAGE" ]]; then
  cd /var/www/front-end/
        echo Missing Stage
        echo $STAGE
        echo Default Mode
        echo Pulling from Bitbucket
        sudo git config --global --add safe.directory /var/www/front-end
        sudo git stash
        sudo git pull origin
        echo Permissions Updated
        sudo chown :www-data sharpdata/db.sqlite3
        sudo chmod 664 sharpdata/db.sqlite3
        echo Database Permissions Updated
        echo Installing Dependencies
        source ~/venv/bin/activate
        pip install -r /var/www/front-end/sharpdata/requirement.txt 
        echo Restarting Apache2 server
        sudo service apache2 restart
        curl -X POST --data-urlencode "payload={\"channel\": \"#datalabz-dev-sprint-deployment\", \"username\": \"EC2_Deployment_Alert\", \"text\": \"Deployed to Default Stage\"}" https://hooks.slack.com/services/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
fi