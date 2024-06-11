# Loopback file

*You don't need this. This is just for fun.*

Idea from: <https://en.wikipedia.org/wiki/Loop_device>

```bash
DATASTORE_DIR=/home
LOOPBACK_FILE=${DATASTORE_DIR}/loopback.img
LOOPBACK_FILE_SIZE=20G
# sparse create (where supported)
fallocate -l ${LOOPBACK_FILE_SIZE} ${LOOPBACK_FILE}
losetup /dev/loop0 ${LOOPBACK_FILE}
mkfs.ext4 /dev/loop0
mkdir -p /loopback
chown nobody:nogroup /loopback
mount /dev/loop0 /loopback
```

Uninstall

```bash
DATASTORE_DIR=/home
LOOPBACK_FILE=${DATASTORE_DIR}/loopback.img
umount /loopback
losetup -d /dev/loop0
rm -rf ${LOOPBACK_FILE}
```
