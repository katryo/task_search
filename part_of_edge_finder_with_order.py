import pdb


class PartOfEdgeFinderWithOrder(object):
    def __init__(self, self_name, nodes, aspect):
        self.task_name = self_name
        self.nodes = nodes
        self.aspect = aspect

    def task_name_shares_url(self):
        my_url = self.aspect['url']
        for node in self.nodes:
            if node[0] == self.task_name:  # 自分自身を見ている
                continue
            aspects = node[1]['aspects']
            if aspects:
                for node_aspect in aspects:
                    your_url = node_aspect['url']
                    if my_url == your_url:  # 自分のエッジとそいつのエッジ、両方ともpart-ofだ
                        return node[0]
        return ''
