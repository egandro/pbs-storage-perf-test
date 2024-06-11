# iSCSI

Ideas from:

- <https://reintech.io/blog/setting-up-iscsi-target-debian-12>
- <https://www.server-world.info/en/note?os=Debian_12&p=iscsi&f=3>
- <https://www.server-world.info/en/note?os=Debian_12&p=iscsi&f=2>
- <https://zahidhaseeb.wordpress.com/2017/03/06/iscsi-target-targetcli-configuration-for-rhelcentos-7x/>
- <https://serverfault.com/questions/258152/fdisk-partition-in-single-line>
- <https://helpdesk.kaseya.com/hc/en-gb/articles/4407512021521-Remove-ISCSI-sessions-using-the-Linux-command-line>

```bash
DATASTORE_DIR=/home
apt update
ISCSI_FILE=${DATASTORE_DIR}/iscsi-storage.img
ISCSI_FILE_SIZE=20G
apt install -y targetcli-fb open-iscsi
targetcli backstores/fileio create name=my_iscsi_storage file_or_dev=${ISCSI_FILE} size=${ISCSI_FILE_SIZE}
targetcli iscsi/ create iqn.2023-01.com.example:storage.target01
targetcli iscsi/iqn.2023-01.com.example:storage.target01/tpg1/portals/ create 0.0.0.0 3260
targetcli iscsi/iqn.2023-01.com.example:storage.target01/tpg1/luns/ create /backstores/fileio/my_iscsi_storage
#targetcli iscsi/iqn.2023-01.com.example:storage.target01/tpg1/acls/ create iqn.2023-01.client:initiator01
NAME=$(cat /etc/iscsi/initiatorname.iscsi | grep '^InitiatorName' | sed -e 's|^InitiatorName=||')
targetcli iscsi/iqn.2023-01.com.example:storage.target01/tpg1/acls/ create "${NAME}"

# mounting
mkdir -p /iscsi
chown nobody:nogroup /iscsi
iscsiadm -m discovery -t st -p 127.0.0.1
iscsiadm -m node --targetname iqn.2023-01.com.example:storage.target01 --portal 127.0.0.1 --login

#show the iscsi disk
iscsiadm -m session -P 3 | grep 'Target\|disk'

#also interessting
#dmesg

# fdisk + format
ISCSI_DEV=/dev/invalid_read_what_iscsiadm_told_you
# danger zone!!!
# we create no partition - just the filesystem on the device
#mkfs.ext4 ${ISCSI_DEV}
#mount ${ISCSI_DEV} /iscsi
```

Uninstall

```bash
DATASTORE_DIR=/home
ISCSI_FILE=${DATASTORE_DIR}/iscsi-storage.img
umount /iscsi
rmdir /iscsi
iscsiadm -m node -T iqn.2023-01.com.example:storage.target01 -p 127.0.0.1 -u
iscsiadm -m node -o delete -T iqn.2023-01.com.example:storage.target01
iscsiadm -m session
iscsiadm -m discoverydb -t sendtargets -p 127.0.0.1 -o delete
#this needs to be empty
ls /var/lib/iscsi/nodes/* || true
systemctl stop iscsid
apt purge -y targetcli-fb open-iscsi
apt autoremove -y
rm -f ${ISCSI_FILE}
```
