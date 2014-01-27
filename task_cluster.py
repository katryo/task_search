# coding:utf-8


class TaskCluster(set):
    def i_cluster_shares_task_with_clusters(self, clusters):
        for task_name in self:
            for i, one_task_cluster in enumerate(clusters):
                if task_name in one_task_cluster:
                    return i
        return -1

