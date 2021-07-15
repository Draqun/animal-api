#!/bin/bash
export APP_HOME=/opt/upskill_backend
yum update -y
yum install -y git
amazon-linux-extras install -y nginx1 python3.8
aws --profile default configure set aws_access_key_id "AKIA46ZQGKPVRU2WG4G5"
aws --profile default configure set aws_secret_access_key "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"
aws s3api get-object --bucket 'dgiebas-upskill-bucket' --key 'ec2temp' ~/.ssh/id_rsa
aws s3api get-object --bucket 'dgiebas-upskill-bucket' --key 'upskillbe.env' /etc/upskillbe.env
chmod 640 /etc/upskillbe.env
chmod 400 ~/.ssh/id_rsa
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone git@gitlab.com:dgiebas/upskill_backend.git
mv upskill_backend/ $APP_HOME
cd $APP_HOME
chmod +x $APP_HOME/resources/run_gunicorn_server.sh
make create-env
make schema-upgrade
cp $APP_HOME/resources/upskill_backend.service /etc/systemd/system
cat > /etc/nginx/conf.d/upskill_backend.conf <<- EOM
server {
    listen 80;
    listen [::]:80;

    access_log /var/log/nginx/reverse-access.log;
    error_log /var/log/nginx/reverse-error.log;

    location / {
        proxy_pass http://unix:/opt/upskill_backend/src/api/webapp/upskill_backend.sock;
    }
}
EOM
. /etc/upskillbe.env && sed -i "s/user:pass@localhost\/db/${DB_USER}:${DB_PASS}@${DB_HOST}\/${DB_NAME}/g" $APP_HOME/db-migrations/alembic.ini
systemctl start upskill_backend.service
systemctl enable upskill_backend.service
systemctl enable nginx
service nginx restart
while [ ! -S /opt/upskill_backend/src/api/webapp/upskill_backend.sock ]
do
  sleep 2 # or less like 0.2
  echo "#" >> /tmp/waiting.tmp
done
chmod 773 /opt/upskill_backend/src/api/webapp/upskill_backend.sock
