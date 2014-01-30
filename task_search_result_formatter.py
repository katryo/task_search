class TaskSearchResultFormatter(object):
    def __init__(self, file_obj, task_type):
        self.file = file_obj
        self.task_type = task_type

    def write_head(self):
        self.file.write('-----\n')
        self.file.write('## %s\n' % self.task_type)
        self.file.write('\n')

