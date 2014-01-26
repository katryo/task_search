# coding:utf-8
import pdb


class PartOfEdgeFinderWithOrder(object):
    def __init__(self, self_name, nodes, url):
        self.task_name = self_name
        self.nodes = nodes
        self.url = url

    def task_name_shares_url(self):
        original_task_names = set()
        for node in self.nodes:
            # 自分自身を選んでもok
            aspects = node[1]['aspects']
            if aspects:
                for node_aspect in aspects:
                    your_url = node_aspect['url']
                    if self.url == your_url:  # 自分のエッジとそいつのエッジ、両方ともpart-ofだ
                        if node_aspect['is_original']:
                            original_task_names.add(node[0])
        return original_task_names
