import pdb


class TaskSearchResultSorter(object):
    def __init__(self, answerer):
        self.instance_ofs = answerer.instance_of_task_clusters_scores
        self.part_ofs = answerer.part_of_task_clusters_scores

    def sorted_by_score(self):
        # 両方を比較して、大きい方を入れる、を繰り返す
        results = []
        for i in range(10):
            if len(self.part_ofs) == 0 and len(self.instance_ofs) == 0:
                break
            if len(self.part_ofs) == 0:
                results.append(self.instance_ofs(0))
                continue
            if len(self.instance_ofs) == 0:
                results.append(self.part_ofs(0))
                continue

            if self._p_is_higher(top_of_i=self.instance_ofs[0],
                                 top_of_p=self.part_ofs[0]):
                results.append((self.part_ofs.pop(0), 'PART-OF'))
            else:
                results.append((self.instance_ofs.pop(0), 'INSTANCE-OF'))
        return results

    def _p_is_higher(self, top_of_i, top_of_p):
        if top_of_p[1] > top_of_i[1]:
            return True
        return False
