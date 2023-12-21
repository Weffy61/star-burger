#!/bin/bash
set -e
cd $1
source venv/bin/activate
git pull
pip install -r requirements.txt
npm ci --dev
python3 manage.py collectstatic
python3 manage.py migrate
systemctl restart star-front.service
systemctl restart star-back.service
systemctl reload nginx.service
echo "Деплой успешно произведен"
