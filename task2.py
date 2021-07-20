import os
import sys
import argparse
import logging
import hashlib

log = logging.getLogger(__name__)
logging.basicConfig(filename='hash_checker.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def read_sum_file(file):
    try:
        with open(file, 'r') as f:
            lines = f.read().splitlines()
        return lines
    except IOError as e:
        log.error('Could not read the input file' + str(e))
        sys.exit('Could not read the input file')


def get_md5_hash(file):
    md5 = hashlib.md5()
    f = open(file, 'rb')
    content = f.read()
    md5.update(content)
    return md5.hexdigest()


def get_sha1_hash(file):
    sha1 = hashlib.sha1()
    f = open(file, 'rb')
    content = f.read()
    sha1.update(content)
    return sha1.hexdigest()


def get_sha256_hash(file):
    sha256 = hashlib.sha256()
    f = open(file, 'rb')
    content = f.read()
    sha256.update(content)
    return sha256.hexdigest()


hash_type_choice = {'md5': get_md5_hash, 'sha1': get_sha1_hash, 'sha256': get_sha256_hash}


def run():
    parser = argparse.ArgumentParser(description='Hash checking program')
    parser.add_argument('file', type=str, metavar='', help='File with stored filenames to check')
    parser.add_argument('location', type=str, metavar='', help='Location (folder) of files to check')
    args = parser.parse_args()
    sum_file, path_to_files = args.file, args.location
    if os.path.isfile(sum_file):
        if os.path.isdir(path_to_files):
            check_lines = read_sum_file(sum_file)
            for check_line in check_lines:
                line = check_line.split()
                for hash_type in hash_type_choice.keys():
                    if line[1] == hash_type:
                        try:
                            current_hash = hash_type_choice[hash_type](path_to_files + '/' + line[0])
                            if current_hash == line[2]:
                                print(line[0] + ' OK')
                            else:
                                print(line[0] + ' FAIL')
                        except FileNotFoundError:
                            print(line[0] + ' NOT FOUND')
        else:
            log.info('No such directory: ' + path_to_files)
            sys.exit('No such directory: ' + path_to_files)
    else:
        log.info('No such file: ' + sum_file)
        sys.exit('No such file: ' + sum_file)


if __name__ == '__main__':
    run()
