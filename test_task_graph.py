#coding: utf-8
import unittest
import pdb
from graph_task_mapper import GraphTaskMapper
from web_page import WebPage
from task_graph_first_answerer import TaskGraphFirstAnswerer
from task_graph_node_remover import TaskGraphNodeRemover


class TestTaskGraph(unittest.TestCase):
    def build_graph(self, pages):
        gtm = GraphTaskMapper()
        for page in pages:
            page.set_sentences_from_text()
            page.set_tasks_from_sentences()
            for task in page.tasks:
                gtm.add_node_and_edge_with_task(task)
        remover = TaskGraphNodeRemover(gtm.graph)
        remover.remove_low_score_generalized_tasks()
        return gtm.graph

    def setUp(self):
        # 適当なWebPage作って、Taskをsetする。
        page_1 = WebPage(url='http://aaa.com', query='職業　質問する')
        page_1.text = '医師に質問してください。'
        page_2 = WebPage(url='http://bbb.com', query='職業　質問する')
        page_2.text = '看護師に質問してください。'
        page_3 = WebPage(url='http://ccc.com', query='職業　質問する')
        page_3.text = '理学療法士に質問してください。'
        self.graph = self.build_graph([page_1, page_2, page_3])

    def test_subtype_of_tasks(self):
        answerer = TaskGraphFirstAnswerer(graph=self.graph, query_task='職業_質問する')
        answerer.set_result_tasks()
        tasks = answerer.subtype_of_tasks
        self.assertEqual(tasks, set(['理学療法士_質問する', '医師_質問する', '看護師_質問する']))

    def test_instance_of_task_clusters_exclude_subtype_of(self):
        answerer = TaskGraphFirstAnswerer(graph=self.graph, query_task='職業_質問する')
        answerer.set_result_tasks()
        clusters = answerer.instance_of_task_clusters
        self.assertEqual(clusters, [])

    def test_part_of_task_clusters(self):
        page = WebPage(url='somewhere', query='カメラ　買う')
        page.text = 'ヨドバシカメラに行く必要があります。お金を払ってください。' \
                    'ヨドバシカメラに行く必要があります。お金を払ってください。'
        graph = self.build_graph([page])
        answerer = TaskGraphFirstAnswerer(graph=graph, query_task='カメラ_買う')
        answerer.set_result_tasks()
        p_clusters = answerer.part_of_task_clusters
        self.assertEqual(p_clusters, [{'お金_払う', 'ヨドバシカメラ_行く'}])

        i_clusters = answerer.instance_of_task_clusters
        self.assertEqual(i_clusters, [])

    def test_instance_of_task_clusters_exclude_part_of(self):
        page_1 = WebPage(url='somewhere', query='チョコレート　食べる')
        page_1.text = 'ヨドバシカメラに行く必要があります。お金を払ってください。' \
                      'ヨドバシカメラに行く必要があります。お金を払ってください。'
        page_2 = WebPage(url='elsewhere', query='チョコレート　食べる')
        page_2.text = '神社にお参りしてください。'
        page_3 = WebPage(url='anywhere', query='チョコレート　食べる')
        page_3.text = '神社にお参りしてください。'
        page_4 = WebPage(url='where', query='チョコレート　食べる')
        page_4.text = 'お金を払いましょう'
        graph = self.build_graph([page_1, page_2, page_3, page_4])
        answerer = TaskGraphFirstAnswerer(graph=graph, query_task='チョコレート_食べる')
        answerer.set_result_tasks()
        i_clusters = answerer.instance_of_task_clusters
        self.assertEqual(i_clusters, [{'神社_お参りする'}])

if __name__ == '__main__':
    unittest.main()
