#!/usr/bin/env python3

import sys

def print_header():
    print("## XXX your Computer Model")
    print()
    print("- CPU: XXX")
    print("- uname: XXX")
    print("- disk model: XXX")
    print("- bonnie++")
    print()
    print("```txt")
    print("```")
    print()

def convert_to_md_table(dump_file):
    f = open(dump_file, "r")
    lines = f.readlines()
    f.close()

    list = []
    entry = dict()

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        arr = line.split(":", 1)
        if arr[0] == "target dir":
            if len(entry) > 0:
                list.append(entry)
            entry = dict()
        entry[arr[0]] = arr[1]
    if len(entry) > 0:
        list.append(entry)
    entry = dict()

    # https://www.markdownguide.org/extended-syntax/
    header_generated=False
    for kvp in list:
        if not header_generated:
            header_generated = True
            count = len(kvp)
            i = 1
            print('|', end='')
            for key in kvp:
                print(' ' + key + ' ', end='')
                if i < count:
                    print('|', end='')
                i = i+1
            print('|')

            i = 1
            print('|', end='')
            for key in kvp:
                print(' --- ', end='')
                if i < count:
                    print('|', end='')
                i = i+1
            print('|')

        count = len(kvp)
        i = 1
        print('|', end='')
        for key in kvp:
            value = kvp[key].strip()
            if key == "target dir":
                value = value.replace('/dummy-chunks', '')
            print(' ' + value + ' ', end='')
            if i < count:
                print('|', end='')
            i = i+1
        print('|')

def main():
    if len(sys.argv) > 1:
        dump_file = sys.argv[1]
        print_header()
        convert_to_md_table(dump_file)

if __name__ == "__main__":
    main()
