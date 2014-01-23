import pdb


class PartOfEdgeFinderWithOrder(object):
    def __init__(self, nodes, aspect):
        self.nodes = nodes
        self.aspect = aspect

    def is_this_aspect_share_url(self):
        my_url = self.aspect['url']
        for node in self.nodes:
            aspects = node[1]['aspects']
            if aspects:
                for node_aspect in aspects:
                    your_url = node_aspect['url']
                    if my_url == your_url:  # 自分のエッジとそいつのエッジ、両方ともpart-ofだ
                        return True
        return False
