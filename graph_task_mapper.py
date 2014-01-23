# -*- coding: utf-8 -*-
import networkx as nx
import pdb
import constants
from hypohype_data_loader import HypoHypeDBDataLoader
from entailment_librarian import EntailmentLibrarian


class GraphTaskMapper():
    def __init__(self, graph=False):
        self.graph = graph or nx.MultiDiGraph()

    def has_stop_object_term(self, object_term):
        stop_words = ['こと', 'もの', 'など']
        if object_term in stop_words:
            return True
        return False

    def _add_new_node(self, object_term, predicate_term, order, url, is_original=False):
        if self.has_stop_object_term(object_term):
            return False

        task_name = '%s_%s' % (object_term, predicate_term)
        new_aspect = {
                'order': order,
                'url': url,
                'is_original': is_original
            }

        if task_name in self.graph.node:
            try:
                old_aspects = self.graph.node[task_name]['aspects']
                new_aspects = old_aspects.append(new_aspect)
            except (KeyError, AttributeError):  # add_edgeでnodeが追加されたあと、nodeとして追加されたときに、ここに来る。
                new_aspects = [new_aspect]
        else:
            new_aspects = [new_aspect]
        self.graph.add_node(task_name, aspects=new_aspects)

    def _add_new_edge(self, task, noun, verb, entailment_type, is_hype):
        if self.has_stop_object_term(noun):
            return False
        if type(noun) == list or type(task.object_term.core_noun) == list:
            pdb.set_trace()
        self.graph.add_edge('%s_%s' %
                            (task.object_term.core_noun, task.predicate_term),
                            '%s_%s' %
                            (noun, verb),
                            entailment_type=entailment_type,
                            is_hype=is_hype)

    def in_degree(self):
        return self.graph.in_degree()

    def add_node_and_edge_with_task(self, task):
        """
        もし1ページ内に順序があればorder=1から始まる値を与える。
        """
        hypes = self._hypes(task)
        nouns = {'hypes': hypes}
        # hypesのときには、edgeにhypeエッジを与える必要ある？　subtype-ofを発見するために。
        original_noun = task.object_term.core_noun
        nouns['original'] = [original_noun]

        original_verb = task.predicate_term
        verbs = self._broader_preds(task)
        verbs['original'] = tuple([original_verb])

        # 上位語・下位語が揃った。
        for hype_type in nouns:
            for noun in nouns[hype_type]:
                if noun == 'ごちゃごちゃ':
                    pdb.set_trace()
                for entailment_type in verbs:  # verbsはdict
                    for verb in verbs[entailment_type]:

                        if noun == original_noun and verb == original_verb:
                            is_original = True
                        else:
                            is_original = False
                        self._add_new_node(object_term=noun,
                                           predicate_term=verb,
                                           order=task.order,
                                           url=task.url,
                                           is_original=is_original)

                        if hype_type == 'hypes':
                            is_hype = True
                        else:
                            is_hype = False
                        self._add_new_edge(task=task,
                                           noun=noun,
                                           verb=verb,
                                           entailment_type=entailment_type,
                                           is_hype=is_hype)

    def _hypes(self, task):
    # object_term.core_nounのhypohypeを探る
        hhdbdl = HypoHypeDBDataLoader()
        hypes = hhdbdl.hypes_except_for_blockwords(task.object_term.core_noun)
        return hypes

    def _broader_preds(self, task):
        librarian = EntailmentLibrarian()
        entailing_predicates = librarian.genaral_from_all_except_for_nonent_ntriv_with_special(task.predicate_term)
        return entailing_predicates  # dict

    def _task_names_in_score_higher_than(self, num=1):
        scores = self.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] > num]
        return results

    def remove_low_score_generalized_tasks(self):
        low_score_generalized_task_names = self._generalized_task_names_in_score_lower_than()
        self.graph.remove_nodes_from(low_score_generalized_task_names)

    def _generalized_task_names_in_score_lower_than(self):
        task_names_lower_in_score = self._task_names_in_score_lower_than()
        results = set()
        for task_name in task_names_lower_in_score:
            aspects = self.graph.node[task_name]['aspects']  # がoriginalだったらcontinue
            is_original = False
            for aspect in aspects:
                if aspect['is_original']:
                    is_original = True
                    break
            if is_original:
                continue
            results.add(task_name)
        return results

    def _task_names_in_score_lower_than(self, num=2):
        scores = self.in_degree()  # {'調味料_ばらまく': 1, ...}
        results = [name for name in scores if scores[name] < num]
        return results

    def _original_task_names_lead_to_higher_score_nodes(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        good_original_task_names = set()
        for generalized_task in task_names_with_higher_score:
            task_names = self.graph.predecessors(generalized_task)
            for task_name in task_names:
                good_original_task_names.add(task_name)
        return good_original_task_names


    # 同じgeneralized_taskにエッジを伸ばす2つのタスク。
    # これらを統合させる必要がある！ g_nodeの名前そのままではなく、
    # 重ね合わせ、集合体として。
    def frequent_tasks_by_generalized_tasks(self):
        task_names_with_higher_score = self._task_names_in_score_higher_than()
        results = dict()
        pdb.set_trace()
        for generalized_task in task_names_with_higher_score:
            good_original_task_names = self.graph.predecessors(generalized_task)
            good_original_tasks = []
            for task_name in good_original_task_names:
                task_attr_dict = self.graph.node[task_name]
                task_attr_dict['name'] = task_name
                good_original_tasks.append(task_attr_dict)

            # もうここにfreqを淹れればよいのでは
            results[generalized_task] = good_original_tasks  # 一見重複しているように見えるタスクかも
        return results  # {'調味料_まく': {name:'塩_ばらまく', url:'http...', 'order': 5 }}
