# Conclusion

## Summary

Mounted datastores in your PBS

- if it's an option - always stay on a local disk - ext4 or zfs doesn't matter
- whatever magic people see in extra performance in zfs, we can't prove it - probably raid on pci4/5 m.2 has extra magic sauce
- webdav is so slow, it isn't even covered by our tests
- avoid nfs and samba like the plague - whatever tutorial you read just ignore it - samba is the worst you can use
- avoid usb - it might be bad for long term stability
- avoid SATA disks
- a very slow ext4 formatted local SATA usb disk might outperform a samba share on a SSD
- if you need remote storage the best you can have is iscsi, FC-SAN or any other remote block device (this is our recommendation for data center users)
- if you have no remote block device, the best recommendation we can give is sshfs (homelab, cheap secondary storage e.g. Hetzner Storage Box)

Virtualized PBS

- it is ok to have your PBS installed as VM and put the virtual datastore disk (the .qcow2 file in Proxmox) on nfs
- check the `loopback-on-nfs` test

## What Proxmox GmbH can do

- give detailed instructions in the PBS documentation to avoid nfs, samba and webdav for pbs mounted datastores (this is simple to implement)
- give some reasons why zfs should be preferred over ext4, our numbers don't show any benefit in zfs so far
- add some indicator to warn if the datastore folder is nfs, samba or webdav (this is simple to implement)
- add a test to measure the performance of the datastore (probably like this, as it is simple to implement)
- introduce a parameter per datastore with the number of buckets to use as they impact read (and in some cases write) performance (Squid uses a different bucket structure - probably they tested this)

In general using the filesystem as database is either a smart or a very bad decision.

## What you can do

Data center

- use local fast SSD disks
- if you want/have to do remote storage, use iscsi / FC-SAN (or any other remote block device)

Homelab

- no nfs, smb
- no exfat
- usb is not super bad (in contrast to nfs, smb)
- SSDs have a much better latency then SATAs (you probably smart and already know that) - no recommendation for SATAs
- if you run your PBS as VM it's more efficient to create a local storage disk and backup the VM (as regular Proxmox Backup) to your nfs / samba / webdav share / SATA drive
- the best remote solution is iscsi / FC-SAN or any other remote block device
- in case you are forced to use a remote fs the only recommendation is sshfs
