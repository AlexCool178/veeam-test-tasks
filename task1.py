import os
import sys
import shutil
import logging
import xml.etree.ElementTree as ETree


log = logging.getLogger(__name__)
logging.basicConfig(filename='copy_module.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def parse_config_file(config_filename):
    try:
        xml_tree = ETree.parse(config_filename)
        return xml_tree
    except FileNotFoundError:
        log.info('Config file not found, check filename or path. Script terminated.')
        sys.exit('Config file not found, check filename or path. Script terminated.')


def get_file_tags(xml_tree):
    root = xml_tree.getroot()
    file_tags = [child for child in root if child.tag == 'file']
    if file_tags:
        return file_tags
    else:
        log.info('Tags <file> not found in config file. Script terminated.')
        sys.exit('Tags <file> not found in config file. Script terminated.')


def get_valid_file_tags(file_tags):
    total = [[e.get('source_path'), e.get('destination_path'), e.get('file_name')] for e in file_tags]
    return [t for t in total if all(t)]


def copy_files(valid_tags):
    if valid_tags:
        for params_to_execute in valid_tags:
            source = params_to_execute[0] + '/' + params_to_execute[2]
            destination = params_to_execute[1] + '/' + params_to_execute[2]
            log.info('Trying to copy %s from %s to %s',
                     params_to_execute[2], params_to_execute[0], params_to_execute[1])
            if os.path.isdir(params_to_execute[0]):
                if os.path.isdir(params_to_execute[1]):
                    if os.path.isfile(source):
                        try:
                            shutil.copyfile(source, destination)
                            log.info('Successfully copied file %s', params_to_execute[2])
                        except PermissionError as e:
                            log.info(str(e))
                    else:
                        log.info('Source file not found')
                        pass
                else:
                    log.info('Destination folder not found')
                    pass
            else:
                log.info('Source folder not found')
    else:
        log.info('No valid tags in config file to operate. Script terminated.')


if __name__ == '__main__':
    tree = parse_config_file('config.xml')
    tags = get_file_tags(tree)
    valid_file_tags = get_valid_file_tags(tags)
    copy_files(valid_file_tags)
