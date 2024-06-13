# Results

*Hint*: The "_no_buckets" columns contains tests (just for fun!) PBS never does such operations.

## Lenovo ThinkPad L13 Gen 2

- CPU: 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz
- uname: Linux 6.1.0-21-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86_64 GNU/Linux
- disk model: nvme-WD_Green_SN350_2TB
- bonnie++

```txt
Version 2.00a       ------Sequential Output------ --Sequential Input- --Random-
                    -Per Chr- --Block-- -Rewrite- -Per Chr- --Block-- --Seeks--
Name:Size etc        /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
lenovo          31G 1975k  99  2.5g  96  1.2g  54 4811k  99  2.4g  66 +++++ +++
Latency              6762us   15395us    9908us    4627us    7630us   37204us
Version 2.00a       ------Sequential Create------ --------Random Create--------
lenovo              -Create-- --Read--- -Delete-- -Create-- --Read--- -Delete--
              files  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
                 16 +++++ +++ +++++ +++ +++++ +++ +++++ +++ +++++ +++ +++++ +++
Latency               252us     179us     679us    1897us      15us     966us
```

| target dir | filesystem detected by stat(1) | files to write | files to read/stat | bucket to create | sha256_name_generation | create_buckets | create_random_files | create_random_files_no_buckets | read_file_content_by_id | read_file_content_by_id_no_buckets | stat_file_by_id | stat_file_by_id_no_buckets | find_all_files | find_all_files_no_buckets |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| . | ext2/ext3 | 500000 | 50000 | 65536 | 0.25s | 1.19s | 10.50s | 13.36s | 4.59s | 2.48s | 3.08s | 1.01s | 8.80s | 1.03s |
| /nfs | nfs | 500000 | 50000 | 65536 | 0.27s | 38.14s | 555.69s | 488.56s | 14.57s | 10.15s | 8.70s | 5.10s | 27.20s | 2.64s |
| /smb | smb2 | 500000 | 50000 | 65536 | 0.30s | 1129.43s | 556.29s | 47923.28s | 49.48s | 38.06s | 45.84s | 34.47s | 222.52s | 11.91s |
| /sshfs | fuseblk | 500000 | 50000 | 65536 | 0.30s | 19.50s | 208.48s | 174.46s | 23.69s | 16.30s | 17.45s | 10.33s | 89.34s | 103.51s |
| /iscsi | ext2/ext3 | 500000 | 50000 | 65536 | 0.26s | 1.87s | 27.53s | 18.15s | 7.63s | 3.14s | 5.28s | 1.10s | 11.39s | 1.50s |
| /ntfs | fuseblk | 500000 | 50000 | 65536 | 0.24s | 1.99s | 52.04s | 60.09s | 18.24s | 6.38s | 12.31s | 3.78s | 58.33s | 0.39s |
| /loopback-on-nfs | ext2/ext3 | 500000 | 50000 | 65536 | 0.25s | 1.50s | 65.18s | 16.09s | 6.45s | 2.06s | 4.03s | 0.97s | 9.55s | 1.03s |


Saturation test

| target dir | filesystem detected by stat(1) | files to write | files to read/stat | buckets | create_random_files | read_file_content_by_id | stat_file_by_id | find_all_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| files-10 | ext2/ext3 | 10 | 10 | 65536 | 0.04s | 0.00s | 0.01s | 0.01s |
| files-100 | ext2/ext3 | 100 | 100 | 65536 | 0.02s | 0.00s | 0.00s | 0.00s |
| files-1000 | ext2/ext3 | 1000 | 1000 | 65536 | 0.05s | 0.03s | 0.03s | 0.03s |
| files-10000 | ext2/ext3 | 10000 | 10000 | 65536 | 0.20s | 0.23s | 0.48s | 0.48s |
| files-100000 | ext2/ext3 | 100000 | 100000 | 65536 | 1.97s | 1.43s | 0.75s | 2.84s |
| files-1000000 | ext2/ext3 | 1000000 | 1000000 | 65536 | 21.47s | 30.79s | 10.55s | 15.75s |
| /smb/files-10 | smb2 | 10 | 10 | 65536 | 0.01s | 0.02s | 0.00s | 0.00s |
| /smb/files-100 | smb2 | 100 | 100 | 65536 | 0.13s | 0.02s | 0.00s | 0.02s |
| /smb/files-1000 | smb2 | 1000 | 1000 | 65536 | 1.08s | 0.36s | 0.16s | 0.21s |
| /smb/files-10000 | smb2 | 10000 | 10000 | 65536 | 10.86s | 8.03s | 7.54s | 2.64s |
| /smb/files-100000 | smb2 | 100000 | 100000 | 65536 | 113.97s | 100.30s | 91.03s | 36.42s |
| /smb/files-1000000 | smb2 | 1000000 | 1000000 | 65536 | 1131.55s | 981.76s | 900.14s | 545.16s |

- disk model: usb-JMicron_Generic (cheap ~2012 usb 2.5" 1TB spinning rust drive)
- bonnie++

```txt
Version 2.00a       ------Sequential Output------ --Sequential Input- --Random-
                    -Per Chr- --Block-- -Rewrite- -Per Chr- --Block-- --Seeks--
Name:Size etc        /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
lenovo          31G 2402k  60 98.3m  14 55.0m  10 4995k  89  119m  12 236.4  10
Latency              4740us   22916us    2047ms   37419us   46581us    1010ms
Version 2.00a       ------Sequential Create------ --------Random Create--------
lenovo              -Create-- --Read--- -Delete-- -Create-- --Read--- -Delete--
              files  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
                 16 16384  98 +++++ +++ +++++ +++ 16384  98 +++++ +++ +++++ +++
Latency              3612us    4317us   19071us    4960us      20us   28522us
```

| target dir | filesystem detected by stat(1) | files to write | files to read/stat | buckets | sha256_name_generation | create_buckets | create_random_files | create_random_files_no_buckets | read_file_content_by_id | read_file_content_by_id_no_buckets | stat_file_by_id | stat_file_by_id_no_buckets | find_all_files | find_all_files_no_buckets |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /usb/ext4 | ext2/ext3 | 500000 | 50000 | 65536 | 0.24s | 1.29s | 34.89s | 13.91s | 398.51s | 102.16s | 611.91s | 85.26s | 715.65s | 96.39s |
| /usb/exfat | exfat | 500000 | 50000 | 65536 | 0.24s | 467.94s | 5926.33s | 73200.98s | 1570.14s | 169.46s | 674.40s | 6.59s | 1180.66s | 31.16s |

## Intel Nuc NUC6i5SYB

- CPU: Intel(R) Core(TM) i5-6260U CPU @ 1.80GHz
- uname: Linux 6.9.3-zabbly+ #debian12 SMP PREEMPT_DYNAMIC Sat Jun  1 04:55:07 UTC 2024 x86_64 GNU/Linux
- disk model: ata-Samsung_SSD_850_EVO_M.2_250GB
- bonnie++

```txt
Version 2.00a       ------Sequential Output------ --Sequential Input- --Random-
                    -Per Chr- --Block-- -Rewrite- -Per Chr- --Block-- --Seeks--
Name:Size etc        /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
nuc             31G  331k  99  290m  77  148m  49  340k  99  511m  83 +++++ +++
Latency             30975us     487ms   41658us   50455us    4011us   20844us
Version 2.00a       ------Sequential Create------ --------Random Create--------
nuc                 -Create-- --Read--- -Delete-- -Create-- --Read--- -Delete--
              files  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP  /sec %CP
                 16 16384  86 +++++ +++ +++++ +++ 16384  96 +++++ +++ +++++ +++
Latency             13499us     809us     903us     164us      29us     617us
```

| target dir | filesystem detected by stat(1) | files to write | files to read/stat | buckets | sha256_name_generation | create_buckets | create_random_files | create_random_files_no_buckets | read_file_content_by_id | read_file_content_by_id_no_buckets | stat_file_by_id | stat_file_by_id_no_buckets | find_all_files | find_all_files_no_buckets |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| . | ext2/ext3 | 500000 | 50000 | 65536 | 0.96 sec | 6.39 sec | 67.58 sec | 45.36 sec | 24.99 sec | 14.12 sec | 10.98 sec | 3.63 sec | 42.25 sec | 2.11 sec |
| /zfs | zfs | 500000 | 50000 | 65536 | 0.51s | 2.43s | 85.24s | 34.08s | 24.86s | 5.45s | 16.52s | 2.87s | 76.11s | 0.58s |
| /nfs | nfs | 500000 | 50000 | 65536 | 1.25 sec | 496.37 sec | 7256.65 sec | 6591.77 sec | 97.60 sec | 51.60 sec | 59.51 sec | 23.32 sec | 189.97 sec | 12.15 sec |
| /smb | smb2 | 500000 | 50000 | 65536 | 0.97s | 3455.01s | 6120.51s | 136370.85s | 171.50s | 114.83s | 169.93s | 113.19s | 1023.71s | 45.74s |
| /sshfs | fuseblk | 500000 | 50000 | 65536 | 0.89 sec | 170.25 sec | 2434.56 sec | 2018.42 sec | 258.87 sec | 166.92 sec | 183.00 sec | 88.34 sec | 1469.04 sec | 339.57 sec |
| /iscsi | ext2/ext3 | 500000 | 50000 | 65536 | 0.91 sec | 8.01 sec | 132.06 sec | 61.64 sec | 49.01 sec | 22.54 sec | 23.55 sec | 7.44 sec | 55.53 sec | 4.84 sec |
