import os


class PathMover(object):
    def go_or_create_and_go_to(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        os.chdir(dirname)

    def go_up(self):
        os.chdir('..')