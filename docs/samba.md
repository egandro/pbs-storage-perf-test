# Samba

## SMB Server

Ideas from:

- <https://reintech.io/blog/installing-configuring-samba-debian-12>
- <https://www.privex.io/articles/how-to-mount-an-smb-share-setup-an-smb-server-on-linux/>

```bash
DATASTORE_DIR=/home
apt update
apt install -y samba samba-common-bin smbclient cifs-utils
systemctl status smbd
cp /etc/samba/smb.conf /etc/samba/smb.conf.backup

mkdir -p ${DATASTORE_DIR}/smbdir
chown nobody:nogroup ${DATASTORE_DIR}/smbdir
chmod 777 ${DATASTORE_DIR}/smbdir

sh -c "cat <<EOF >> /etc/samba/smb.conf
[smbdir]
   path = ${DATASTORE_DIR}/smbdir
   hosts allow = 127.0.0.1
   writable = yes
   guest ok = yes
   public = yes
   create mask = 0664
   directory mask = 0775
   force user = nobody

EOF"

systemctl restart smbd
smbclient -L localhost -U %

# mounting
mkdir -p /smb
chown nobody:nogroup /smb
mount -v -t cifs //127.0.0.1/smbdir -o guest /smb
```

Uninstall

```bash
DATASTORE_DIR=/home
umount /smb
rmdir /smb
systemctl stop smbd
rm -rf ${DATASTORE_DIR}/smbdir
apt purge -y samba samba-common-bin smbclient cifs-utils
apt autoremove -y
rm -rf /etc/samba
```
