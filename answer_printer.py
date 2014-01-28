class AnswererPrinter(object):
    def __init__(self, answerer):
        self.answerer = answerer

    def ourput_part_of_tasks(self):
        for task_set in self.answerer.part_of_task_clusters_scores:
            with open()