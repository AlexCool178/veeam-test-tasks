import os
import sys
import shutil
import xml.etree.ElementTree as ETree


def parse_config_file(config_filename):
    try:
        xml_tree = ETree.parse(config_filename)
        return xml_tree
    except FileNotFoundError:
        print('Config file not found, check filename or path. Script terminated.')
        sys.exit()


def get_file_tags(xml_tree):
    root = xml_tree.getroot()
    file_tags = [child for child in root if child.tag == 'file']
    if len(file_tags) > 0:
        return file_tags
    else:
        print('Tags <file> not found in config file. Script terminated.')
        sys.exit()


def get_valid_file_tags(file_tags):
    total = [[e.get('source_path'), e.get('destination_path'), e.get('file_name')] for e in file_tags]
    return [t for t in total if all(t)]


def copy_files(valid_tags):
    if valid_tags:
        for params_to_execute in valid_tags:
            source = params_to_execute[0] + '/' + params_to_execute[2]
            destination = params_to_execute[1] + '/' + params_to_execute[2]
            print(f'Trying to copy {params_to_execute[2]} from {params_to_execute[0]} to {params_to_execute[1]}')
            if os.path.isdir(params_to_execute[0]):
                if os.path.isdir(params_to_execute[1]):
                    if os.path.isfile(source):
                        try:
                            shutil.copyfile(source, destination)
                            print(f'Successfully copied file {params_to_execute[2]}')
                        except PermissionError as e:
                            print(str(e))
                    else:
                        print('Source file not found')
                        pass
                else:
                    print('Destination folder not found')
                    pass
            else:
                print('Source folder not found')
    else:
        print('No valid tags in config file to operate. Script terminated.')


if __name__ == '__main__':
    tree = parse_config_file('config.xml')
    tags = get_file_tags(tree)
    valid_file_tags = get_valid_file_tags(tags)
    copy_files(valid_file_tags)
