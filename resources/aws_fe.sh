#!/bin/bash
yum update -y
yum install -y git
amazon-linux-extras install -y nginx1
aws --profile default configure set aws_access_key_id "AKIA46ZQGKPVRU2WG4G5"
aws --profile default configure set aws_secret_access_key "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"
aws s3api get-object --bucket 'dgiebas-upskill-bucket' --key 'ec2temp' ~/.ssh/id_rsa
chmod 400 ~/.ssh/id_rsa
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
PUB_URL=`curl ipinfo.io/ip`
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone git@gitlab.com:dgiebas/upskill_frontend.git
sed -i "s/127.0.0.1:8000/${PUB_URL}/g" upskill_frontend/js/app.js
echo "location /api { proxy_pass http://internal-dgiebas-upskill-purivlb-1605436538.eu-west-1.elb.amazonaws.com; }" >> /etc/nginx/default.d/server-proxy.conf
cp -ufR upskill_frontend/* /usr/share/nginx/html/
systemctl enable nginx
service nginx restart
