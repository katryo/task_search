#coding: utf-8
import unittest
import pdb
from graph_task_mapper import GraphTaskMapper
from web_page import WebPage
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_graph_node_remover import TaskGraphNodeRemover


class TestTaskGraph(unittest.TestCase):
    def setUp(self):
        # 適当なWebPage作って、Taskをsetする。
        page_1 = WebPage(url='http://aaa.com', query='職業　質問する')
        page_1.text = '医師に質問してください。'
        page_2 = WebPage(url='http://bbb.com', query='職業　質問する')
        page_2.text = '看護師に質問してください。'
        page_3 = WebPage(url='http://ccc.com', query='職業　質問する')
        page_3.text = '理学療法士に質問してください。'

        gtm = GraphTaskMapper()
        for page in [page_1, page_2, page_3]:
            page.set_sentences_from_text()
            page.set_tasks_from_sentences()
            for task in page.tasks:
                gtm.add_node_and_edge_with_task(task)
        remover = TaskGraphNodeRemover(gtm.graph)
        remover.remove_low_score_generalized_tasks()

        self.graph = gtm.graph

    def test_subtype_of_tasks(self):
        answerer = TaskGraphFirstAnswerer(graph=self.graph, query_task='職業_質問する')
        answerer.set_result_tasks()
        tasks = answerer.subtype_of_tasks
        self.assertEqual(tasks, set(['理学療法士_質問する', '医師_質問する', '看護師_質問する']))

    def _test_instance_of_task_clusters(self):
        print('!?!?!?!?!?!')
        answerer = TaskGraphFirstAnswerer(graph=self.graph, query_task='職業_質問する')
        answerer.set_result_tasks()
        clusters = answerer.instance_of_task_clusters
        self.assertEqual(clusters, [('病院_行く', '医師_相談', '看護師_質問',)])

if __name__ == '__main__':
    unittest.main()
