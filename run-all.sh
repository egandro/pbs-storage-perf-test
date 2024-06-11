#!/bin/bash

files_to_write=500000
files_to_read=50000

declare -a dirs=("" "/nfs" "/smb" "/sshfs" "/iscsi")

for dir in "${dirs[@]}"
do
	./create_random_chunks.py "${dir}" ${files_to_write} ${files_to_read}
	echo ""
done


#DATASTORE_DIR=/home
#sudo rm -rf ./dummy-chunks ${DATASTORE_DIR}/nfsdir/dummy-chunks ${DATASTORE_DIR}/smbdir/dummy-chunks ${DATASTORE_DIR}/sshfsdir/dummy-chunks /iscsi/dummy-chunks
