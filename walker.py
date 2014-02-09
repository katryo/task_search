import os
import pdb


class Walker(object):
    def convert_quotations(self, path):
        result = str()
        with open(path, 'r') as f:
            for row in f:
                result += row
        tex_pathname = path.replace('.txt', '.tex')
        with open(tex_pathname, 'w') as f:
            f.write(result)

    def move(self, target_type):
        for dirpath, dirnames, filenames in os.walk(target_type):
            for filename in filenames:
                if '.txt' in filename:
                    path = os.path.join(dirpath, filename)

            for dirname in dirnames:
                for d_dirpath, d_dirnames, d_filenames in os.walk('src/%s' % dirname):
                    for d_filename in d_filenames:
                        if '.txt' in d_filename:
                            path = os.path.join(d_dirpath, d_filename)

