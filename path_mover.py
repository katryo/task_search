import os
import pdb


class PathMover(object):
    def go_or_create_and_go_to(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        try:
            os.chdir(dirname)
        except NotADirectoryError:
            pdb.set_trace()

    def go_up(self):
        os.chdir('..')