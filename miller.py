import os
import argparse


parser = argparse.ArgumentParser(description="A simple script to check for forbidden functions in C files.")
parser.add_argument(
    '--path', type=str, 
    help='(optional) The path to the directory to check for forbidden functions, default is current directory'
)
# parser.add_argument('--ignore-directory', type=list, help='(optional) List of directories to ignore')


forbidden = set([
    'strlen',
    'strchr',
    'strrchr',
    'strstr',
    'strtok',
    'strtok_r',
    'strdup',
    'strndup',
    'strcpy',
    'strncpy',
    'strlcpy',
    'strcat',
    'strncat',
    'sprintf',
    'vsprintf',
    'snprintf',
    'vsnprintf',
    'memcpy',
    'memmove',
    'memcmp',
    'memset',
    'memchr',
    'memrchr',
    'memmem',
    'memccpy',
    'bcopy',
    'bzero',
    'index',
    'rindex',
    'strpbrk',
    'strspn',
    'strcspn',
    'strjoin',
    'strnjoin',
    'strsub',
    'strnsub',
    'strreplace',
    'strnreplace',
    'strcase',
    'atoi',
    'atol',
    'atoll',
    'isdigit',
    'isalpha',
    'isalnum',
    'islower',
    'isupper',
    'isspace',
    'split',
    'splitstr',
    'strmapi',
    'strmap',
    'strtrim',
])


def get_all_c_files(path):
    """
    Get all .C files in current and subdirectories
    """
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.c'):
                files.append(os.path.join(root, filename))
    print("Number of files: ", len(files))
    return files

def is_commented_out(line, func):
    """
    Check if line is commented out
    """
    index = str(line).index(func)
    if index == -1:
        return False
    try:
        has_double_slash = line[0:index].index('//') 
        if has_double_slash == 0:
            return True
        if has_double_slash != -1 and line[0:has_double_slash].isspace():
            return True
    except ValueError:
        return False


def check_file(file):
    """
    Check if file contains forbidden functions
    """
    forbidden_count = 0
    line_number = 0
    with open(file, 'r') as f:
        for line in f:
            line_number += 1
            for func in forbidden:
                if f' {func}(' in line or f' {func} (' in line:
                    if is_commented_out(line, func):
                        continue
                    print(f'\033[91m{file}\033[0m')
                    print(f'  Line {line_number}: {line.strip()}')
                    forbidden_count += 1
    if forbidden_count > 0:
        print(f'\033[93m{forbidden_count} forbidden functions found.\033[0m\n')
    else:
        print(f'{file} \033[92mOK\033[0m\n')


def main(*args):
    path = '.'
    args = parser.parse_args()
    print(f"Path: {args.path}")
    path = args.path
    for file in get_all_c_files(path):
        check_file(file)

main()
