#coding: utf-8
import pdb


class AnswererPrinter(object):
    def __init__(self, answerer, query):
        self.results = answerer.united_results
        self.query = query

    def output(self, method_name=''):
        with open('%s_%s_result.md' % (self.query, method_name), 'w') as f:
            self.file = f
            self._write_title()
            self._write_with_list()

    def _write_with_list(self):
        num_of_writing = 0
        for result in self.results:
            task_cluster = result[0]
            self.file.write('\n')
            try:
                score = str(task_cluster[1])
            except:
                pdb.set_trace()
            self.file.write('### SCORE: %s\n' % score)
            self._write_header_with_task_type(result[1])
            for task_name in task_cluster[0]:
                self.file.write('- %s \n' % task_name)
            num_of_writing += 1
            self._write_footer()
            if num_of_writing > 9:
                break

    def _print_with_subtype_of(self, set_obj):
        for item in set_obj:
            self.file.write(item + '\n')

    def _write_header_with_task_type(self, task_type):
        self.file.write('#### %s\n' % task_type)
        self.file.write('\n')

    def _write_footer(self):
        self.file.write('\n----------\n')

    def _write_title(self):
        self.file.write('## クエリ 「%s」\n' % self.query)
