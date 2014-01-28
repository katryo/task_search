#coding: utf-8
from path_mover import PathMover


class AnswererPrinter(object):
    def __init__(self, answerer, query):
        self.answerer = answerer
        self.query = query

    def ourput(self, method_name=''):
        pm = PathMover()
        pm.go_or_create_and_go_to('results')
        with open('%s_%s_result.txt' % (self.query, method_name), 'w') as f:
            f.write('part-of')
            f.writelines(self.answerer.part_of_task_clusters_scores)
            f.write('instance-of')
            f.writelines(self.answerer.instance_of_task_clusters_scores)
            f.write('subtype-of')
            f.writelines(self.answerer.subtype_of_tasks)
        pm.go_up()
