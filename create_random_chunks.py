#!/usr/bin/env python3

import hashlib
import os
import time
import sys
import subprocess

FILES_TO_WRITE = 500000
FILES_TO_READ = 50000
BASE_DIR= "dummy-chunks"

def function_time(func):
	def wrapper(*args, **kwargs):
		start = time.time()
		func(*args, **kwargs)
		end = time.time()
		sec = end - start
		delta = '{:.2f}'.format(sec)
		print(func.__name__+":", delta + "s")
	return wrapper

# drops the linux filesystem cache
# idea from: https://unix.stackexchange.com/questions/87908/how-do-you-empty-the-buffers-and-cache-on-a-linux-system
def drop_caches():
    filename = "/proc/sys/vm/drop_caches"
    states = [1, 2, 3]
    for state in states:
      try:
        f = open(filename, "w")
        f.write(str(state))
        f.close()
      except PermissionError as err:
        print("can't drop flush the linux filesystem caches - you need to start to program as root")
        print(err)
        exit(1)

# speed test of the sha256 function
@function_time
def sha256_name_generation():
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_WRITE):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      prefix = sha[0:4]
      filename = BASE_DIR + "/buckets/" + prefix + "/" + sha
      #print(filename)

@function_time
def create_buckets():
    bucket_count = 64 * 1024 # 0000 - ffff
    for x in range(bucket_count):
        dir_name = '{:04x}'.format(x)
        path = BASE_DIR + "/buckets/" + dir_name
        #print(path)
        try:
            os.makedirs(path, 0o755)
        except OSError as err:
            print("directory already exists - please cleanup the folder")
            print(err)
            exit(1)

@function_time
def create_random_files():
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_WRITE):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      prefix = sha[0:4]
      filename = BASE_DIR + "/buckets/" + prefix + "/" + sha
      f = open(filename, "w")
      f.write(str(x))
      f.close()

@function_time
def create_random_files_no_buckets():
    path = BASE_DIR + "/" + "no_buckets"
    try:
        os.makedirs(path, 0o755)
    except OSError as err:
        print("directory already exists - please cleanup the folder")
        print(err)
        exit(1)

    sha256 = hashlib.sha256()
    for x in range(FILES_TO_WRITE):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      filename = path + "/" + sha
      f = open(filename, "w")
      f.write(str(x))
      f.close()

@function_time
def read_file_content_by_id():
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_READ):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      prefix = sha[0:4]
      filename = BASE_DIR + "/buckets/" + prefix + "/" + sha
      f = open(filename, "r")
      bytes = f.read()
      #print(str(bytes))
      f.close()

@function_time
def read_file_content_by_id_no_buckets():
    path = BASE_DIR + "/" + "no_buckets"
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_READ):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      filename = path + "/" + sha
      f = open(filename, "r")
      bytes = f.read()
      #print(str(bytes))
      f.close()

@function_time
def stat_file_by_id():
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_READ):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      prefix = sha[0:4]
      filename = BASE_DIR + "/buckets/" + prefix + "/" + sha
      fd = os.open(filename, os.O_RDONLY)
      stat = os.fstat(fd)
      #print(stat)
      os.close(fd)

@function_time
def stat_file_by_id_no_buckets():
    path = BASE_DIR + "/" + "no_buckets"
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_READ):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      filename = path + "/" + sha
      fd = os.open(filename, os.O_RDONLY)
      stat = os.fstat(fd)
      #print(stat)
      os.close(fd)

@function_time
def find_all_files():
    sha256 = hashlib.sha256()
    for x in range(FILES_TO_WRITE):
      sha256.update(str(x).encode())
      sha = sha256.hexdigest()
      prefix = sha[0:4]
      path = BASE_DIR + "/buckets/" + prefix
      listdir = os.listdir(path)
      #print(listdir)

@function_time
def find_all_files_no_buckets():
    path = BASE_DIR + "/" + "no_buckets"
    listdir = os.listdir(path)
    #print(listdir)

def show_info():
    print("target dir:", BASE_DIR)

    # get the basedir
    path=BASE_DIR
    i = path.rindex("/")
    path = path[0:i+1]

    # stat -f -c %T /your/dir
    result = subprocess.run(['/usr/bin/stat', '-f', '-c', '%T', path], stdout=subprocess.PIPE)
    filesystem = str(result.stdout.decode('utf-8')).strip()
    print("filesystem detected by stat(1):", filesystem)

    print("files to write:", FILES_TO_WRITE)
    print("files to read/stat:", FILES_TO_READ)
    print("buckets:", 64 * 1024)

def main():
    show_info()
    sha256_name_generation()
    drop_caches()
    create_buckets()
    drop_caches()
    create_random_files()
    drop_caches()
    create_random_files_no_buckets()
    drop_caches()
    read_file_content_by_id()
    drop_caches()
    read_file_content_by_id_no_buckets()
    drop_caches()
    stat_file_by_id()
    drop_caches()
    stat_file_by_id_no_buckets()
    drop_caches()
    find_all_files()
    drop_caches()
    find_all_files_no_buckets()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        BASE_DIR="./" + BASE_DIR
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path == "":
            path = "."
        BASE_DIR=path + "/" + BASE_DIR
    if len(sys.argv) > 2:
        FILES_TO_WRITE = sys.argv[2]
        if FILES_TO_WRITE == "":
            FILES_TO_WRITE = FILES_TO_WRITE
        FILES_TO_WRITE = int(FILES_TO_WRITE)
    if len(sys.argv) > 3:
        FILES_TO_READ = sys.argv[3]
        if FILES_TO_READ == "":
            FILES_TO_READ = FILES_TO_READ
        FILES_TO_READ = int(FILES_TO_READ)
        if FILES_TO_READ > FILES_TO_WRITE:
            FILES_TO_READ = FILES_TO_WRITE
    main()
