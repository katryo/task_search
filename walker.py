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

    def move(self, target_dirname):
        # target_dirname => 'fetched_pages' or 'graph'
        for dirpath, dirnames, filenames in os.walk(target_dirname):
            for dirname in dirnames:
                # dirname => '花粉症　対策する'
                deeper_dirname = os.path.join(target_dirname, dirname)
                for d_dirpath, d_dirnames, d_filenames in os.walk(deeper_dirname):
                    for d_filename in d_filenames:
                        if '.pkl' in d_filename:
