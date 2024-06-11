# PBS Storage Performance Tester

This wil simulate read/write operations done by the [Proxmox Backup Server](https://www.proxmox.com/en/proxmox-backup-server/overview) (PBS).

There are a lot of myths and bad YouTube tutorials what filesystem to use.

So here is a software that allows testing what local or remote filesystem is best for you.

## Fast tack

- [results](/results.md)
- [conclusion](/conclusion.md)

## What you need for your own performance tests

- a PBS installation
- or a Debian 12 installation (which PBS is currently based on)
- you can use / install any filesystem that you like (ext4, btrfs, zfs, ...)
- python3 and basic os tools

## Create remote filesystems

This test contains instructions on how to setup (localhost) servers for

- [nfs](/docs/nfs.md)
- [samba](/docs/samba.md)
- [sshfs](/docs/sshfs.md)
- [iscsi](/docs/iscsi.md)
- [webdav](/docs/webdav.md) (this is so slow, even the bucket creation took >= 90 minutes)
- [loopback](/docs/loopback.md) (playground - serves no purpose - you don't need this)

(Feel free send a pull request with instructions if you want to have any other fs not covered here - or - if you think there are performance enhancements possible by better configuration settings.)

We want to compare filesystems - we are not interested in measuring the speed of a network.

For this reason, we use localhost/localhost connections.

*Security*: best effort has been put in the instructions to allow localhost only connections. There might be other risks we didn't cover here. Don't use public IPs!

*Sanity Check*: Do not create random remote filesystems on your production PBS. Create a test installation. Do not run the uninstall instructions on your production PBS.

## How PBS uses the filesystem

Organization

- PBS uses datastore directory
- Bucket directories .chunk/0000 to .chunk/ffff (65536 directories)
- A chunk name is a sha256 checksum e.g. 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 (64 characters)
- You might have 100.000 or 500.000 or millions of these files in your datastore (depending on your setup)

Operations

- PBS reads,writes,deletes a file
- PBS fstat(2) a file (size, modification time, ...)
- PBS tries to find all files in the datastore directory e.g. garbage collect by using opendir(3) and readdir(3)

## What do we test

- What is the performance of the sha256 function?
- Create the buckets (0000-ffff)
- Create n random files with sha256 names and store them in their buckets. We write a simple integer as file content
- Read x random files by their sha256 name
- Stat x random files by their sha256 name
- Find all files in the data directory

Just for fun

- Create n random files (same as before - not using bucket subdirectories)
- Read x random files (same as before - not using bucket subdirectories)
- Stat x random files (same as before - not using bucket subdirectories)
- Find all files (same as before - not using bucket subdirectories)

## How do we test?

- Now threading - single process - single thread python. We are interested in the worst case.
- Times are simple python times (time.time() deltas). That are system, kernel, process "real world" times.
- Linux buffers and caches are cleared via /proc/sys/vm/drop_caches before each test. So we don't benchmark your ram. The idea is taken from [here](https://unix.stackexchange.com/questions/87908/how-do-you-empty-the-buffers-and-cache-on-a-linux-system).
- *Security* only root can write to /proc/sys/vm/drop_caches.

## Run a simple test on your local disk / the disk you already mounted

Run

```bash
sudo ./create_random_chunks.py .
# or
sudo ./create_random_chunks.py /datastoreFoo
```

Cleanup

```bash
sudo rm -rf ./dummy-chunks
# or
sudo rm -rf /datastoreFoo//dummy-chunks
```

## Run all tests for all remote filesystems

You need to setup the remote filesystems as described [here](#create-remote-filesystems).

```bash
# check or modify the paths in here: run-all.sh
# this takes ~ 12h on my nuc
sudo ./run-all.sh >dump.txt
```

Cleanup

```bash
#DATASTORE_DIR=/home
#sudo rm -rf ./dummy-chunks ${DATASTORE_DIR}/nfsdir/dummy-chunks ${DATASTORE_DIR}/sshfsdir/dummy-chunks ${DATASTORE_DIR}/sshfsdir/dummy-chunks /iscsi/dummy-chunks
```

Uninstall the filesystems as described [here](#remote-filesystems).

*Security* only root can write to /proc/sys/vm/drop_caches.

## Send us your results

### Detect the hardware you are running on

Computer

(this might not work - then type it!)

```bash
sudo dmidecode | grep -A3 '^System Information'
```

CPU

```bash
lscpu | grep "Model name" | sed -e "s|^.*:\s*||"
```

uname (without the hostname)

```bash
uname -s -r -v -m -o
```

Disk

```bash
ls /dev/disk/by-id | grep -v part | grep -v "_1" | grep -v "md-"
```

- if you see a "QEMU", "VBOX", "VMware" you are running on a vm
- these names follow a pattern
  - type-manufacturer-model-serial
    - type: ata, scsi, nvme, ...
    - manufacturer: Toshiba, Samsung, ...
    - model: your drive model
    - serial: 123456789
- in case you have many disks (or zfs, or raid, ...) - pick one - of your datastore
- *Security* Only send us type-manufacturer-model. No not send us your serial number of your disk!

### Disk benchmark

You will need a lot of disk space!

```bash
DATASTORE_DIR=/home

sudo apt-get install bonnie++
sudo /usr/sbin/bonnie -u root -d ${DATASTORE_DIR}
```

### Create a table from your dump.txt file

```bash
./result-to-markdown.py dump.txt > result.md
# fill in the cpu, uname, disk model and bonnie++ section
# create a PR
```
