kill `cat /tmp/logjam.pid `
sudo /etc/init.d/apache2 restart
sudo /etc/init.d/postfix restart
./manage.py logserver
