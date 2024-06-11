# Webdav

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
This is too slow to test.
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Idea from

- <https://kb.interspace.com/en/tech-articles/tutorials/setup-webdav-server-with-nginx-on-debian>
- <https://wiki.hpc.rug.nl/rdms/access/linux/webdav>

```bash
DATASTORE_DIR=/home
username=webdav
password=webdav

apt update
apt install -y nginx nginx-extras davfs2

mkdir -p ${DATASTORE_DIR}/webdav/data
mkdir -p ${DATASTORE_DIR}/webdav/tmp
chown -R www-data:www-data ${DATASTORE_DIR}/webdav/data
chown -R www-data:www-data ${DATASTORE_DIR}/webdav/tmp
chmod -R 755 ${DATASTORE_DIR}/webdav/data
chmod -R 755 ${DATASTORE_DIR}/webdav/tmp

echo "$username:$(openssl passwd -apr1 $password)" | tee -a /etc/nginx/webdav.passwd > /dev/null

cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.orig

cat <<EOF > /etc/nginx/sites-available/default

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                try_files \$uri \$uri/ =404;
        }

        location /webdav {
            alias ${DATASTORE_DIR}/webdav/data;
            client_body_temp_path ${DATASTORE_DIR}/webdav/tmp;
            dav_methods PUT DELETE MKCOL COPY MOVE;
            dav_ext_methods PROPFIND OPTIONS;
            create_full_put_path on;

            auth_basic "Restricted Access";
            auth_basic_user_file /etc/nginx/webdav.passwd;

            satisfy all;
            allow 127.0.0.1;
            deny all;
        }
}

EOF

systemctl restart nginx

# mounting
mkdir -p /webdav
chown nobody:nogroup /webdav
mount.davfs -o users,uid=systemuser,username=${username} http://127.0.0.1/webdav /webdav
```

Uninstall

```bash
DATASTORE_DIR=/home
umount /webdav
rmdir /webdav
systemctl stop nginx
apt purge -y nginx nginx-extras davfs2
rm -rf /var/cache/davfs2
rm -rf ${DATASTORE_DIR}/webdav
apt autoremove -y
```
