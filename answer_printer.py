#coding: utf-8
import pdb
import constants


class AnswererPrinter(object):
    def __init__(self, answerer, query):
        self.results = answerer.united_results
        self.query = query
        self.simple_results = answerer.simple_results

    def output(self, method_name=''):
        with open('%s_%s_result.md' % (self.query, method_name), 'w') as f:
            self.file = f
            self._write_title()
            self._write_simple_results()
            # self._write_with_list()

    def _write_simple_results(self):
        for i, simple_result in enumerate(self.simple_results):
            if simple_result:
                self.file.write('%i\n\n' % i)
                for task_name in simple_result:
                    self.file.write('- %s \n' % task_name.replace('_', ''))
                self.file.write('\n\n')


    def _write_with_list(self):
        num_of_writing = 0
        diversity = 0
        num_of_subtypes = 0
        did_write_supertype = False
        for result in self.results:
            task_cluster = result[0]
            self.file.write('\n')
            try:
                score = str(task_cluster[1])
            except:
                continue  # 答えが10ないとき
            #self.file.write('### SCORE: %s\n' % score)
            self._write_header_with_task_type(result[1])
            if result[1] == 'PART-OF':
                try:
                    self._write_subtype(result[0][2])  # urlかsubtypeかを出力
                    if type(result[0][2]) == str:
                        num_of_subtypes += 1
                        print('subtype')
                    else:
                        if not did_write_supertype:
                            num_of_subtypes += 1
                            did_write_supertype = True
                            print('super')
                except IndexError:
                    self._write_subtype(constants.SUPERTYPE_NAME)
            self._write_num_of_tasks(len(task_cluster[0]))
            for task_name in task_cluster[0]:
                self.file.write('- %s \n' % task_name)
            num_of_writing += 1
            diversity += num_of_subtypes
            self._write_footer()
            if num_of_writing > 9:
                break
        self._write_diversity(diversity)

    def _write_diversity(self, num):
        self.file.write('##### Diversity %i\n' % num)
        self.file.write('\n')

    def _write_num_of_tasks(self, size):
        self.file.write('##### タスク数%i\n' % size)
        self.file.write('\n')

    def _print_with_subtype_of(self, set_obj):
        for item in set_obj:
            self.file.write(item + '\n')

    def _write_subtype(self, subtype):
        self.file.write('##### %s\n' % subtype)
        self.file.write('\n')

    def _write_header_with_task_type(self, task_type):
        self.file.write('#### %s\n' % task_type)
        self.file.write('\n')

    def _write_footer(self):
        self.file.write('スコアを書いてね☆=>\n')
        self.file.write('\n----------\n')

    def _write_title(self):
        self.file.write('## クエリ 「%s」\n' % self.query)
