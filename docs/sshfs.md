# SSHFS

Idea from: <https://www.server-world.info/en/note?os=Debian_12&p=ssh&f=8>

Setup your SSH keys

```bash
DATASTORE_DIR=/home
SSH_USER=root
apt update
apt install -y sshfs

mkdir -p ${DATASTORE_DIR}/sshfsdir
chown nobody:nogroup ${DATASTORE_DIR}/sshfsdir
chmod 777 ${DATASTORE_DIR}/sshfsdir

# mounting
mkdir -p /sshfs
chown nobody:nogroup /sshfs
sshfs ${SSH_USER}@127.0.0.1:${DATASTORE_DIR}/sshfsdir /sshfs
```

Uninstall

```bash
DATASTORE_DIR=/home
umount /sshfs
rmdir /sshfs
rm -rf ${DATASTORE_DIR}/sshfsdir
apt purge -y sshfs
apt autoremove -y
```
