import os
import sys
import re
from shutil import copyfile
import EList

e_list = EList()
match = r'(^ +|".*"| [^ "]* )'


def processFile(infile, outfile):
    global e_list
    global match
    outfile.write('\n')
    for line in infile:
        if line.startswith("#"):
            outfile.write(line)
            continue
        for token in re.split(match, line.strip('\n\r')):
            if not token:
                continue
            if e_list.check_token(token):
                outfile.write(e_list.get_e(token))
            else:
                position = outfile.tell()
                e_list.add_e(token)
                insert = e_list.get_e_define(token)

                outfile.seek(0, 0)
                content = outfile.read()
                outfile.seek(0, 0)
                outfile.write(insert.rstrip('\r\n') + '\n' + content)
                outfile.seek(0, 2)
                outfile.write(e_list.get_e(token))
            outfile.write(' ')
        outfile.write('\n')



if __name__ == "__main__":
    for root, dirs, files in os.walk(sys.argv[1]):
        # https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
        dirs[:] = [d for d in dirs if d != 'e']

        e_root = os.path.join(root, 'e')
        if not os.path.exists(e_root):
            os.mkdir(e_root)
        for directory in dirs:
            if not os.path.exists(os.path.join(e_root, directory)) \
                and not directory.startswith('.') \
                and not 'e':
                os.mkdir(os.path.join(e_root, directory))
        for file in files:
            endpath = os.path.join(e_root, file)
            if file.endswith(".c") or file.endswith(".h"):
                file_o = open(os.path.join(root, file), "r")
                if not os.path.exists(endpath):
                    os.mknod(endpath)
                file_e = open(endpath, "r+w")
                file_e.truncate(0)
                processFile(file_o, file_e)
                file_o.close()
            else:
                copyfile(os.path.join(root, file), endpath)