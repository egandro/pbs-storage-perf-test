# NFS

Idea from <https://reintech.io/blog/setting-up-nfs-server-on-debian-12>

```bash
DATASTORE_DIR=/home
apt update
apt install -y nfs-kernel-server
mkdir -p ${DATASTORE_DIR}/nfsdir
chown nobody:nogroup ${DATASTORE_DIR}/nfsdir
sh -c "echo '${DATASTORE_DIR}/nfsdir 127.0.0.1/(rw,sync,no_subtree_check)' >> /etc/exports"
exportfs -a
systemctl restart nfs-kernel-server

# mounting
mkdir -p /nfs
chown nobody:nogroup /nfs
mount 127.0.0.1:${DATASTORE_DIR}/nfsdir /nfs
```

Uninstall

```bash
DATASTORE_DIR=/home
umount /nfs
rmdir /nfs
systemctl stop nfs-kernel-server
rm -rf ${DATASTORE_DIR}/nfsdir
apt purge -y nfs-kernel-server
apt autoremove -y
```
