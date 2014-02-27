# -*- coding: utf-8 -*-
import pdb
from graph_task_mapper import GraphTaskMapper
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from task_data_selector import TaskDataSelector
from task_subtype_data_loader import TaskSubtypeDataLoader
import constants
from task import Task


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfs = PickleFileSaverForOriginal()
    pfl = PickleFileLoaderForOriginal()
    gtm = GraphTaskMapper()
    with TaskDataSelector() as selector:
        for query in original_queries:
            task_ids = selector.task_ids_with_query(query)
            for task_id in task_ids:
                with TaskSubtypeDataLoader() as task_subtype_loader:
                    distance_subtype_pairs = task_subtype_loader.distance_from_subtype_with_task_id(task_id)
                    distance_between_subtypes = {}
                    for pair in distance_subtype_pairs:
                        distance_between_subtypes[pair[0]] = pair[1]

                    task_data = selector.taskdata_with_task_id(task_id)
                    try:
                        task = Task(distance_between_subtypes=distance_between_subtypes,
                                    object_term=task_data[0],
                                    cmp=task_data[1],
                                    predicate_term=task_data[2],
                                    order=task_data[3],
                                    query=task_data[4],
                                    url=task_data[5],
                                    rank=task_data[6]
                                    )
                        gtm.add_node_and_edge_with_task(task)
                    except IndexError:
                        pdb.set_trace()
                        print('aaa')
            pfs.save_graph_with_query(obj=gtm.graph, query=query)
