# -*- coding: utf-8 -*-
__author__ = 'katouryou'
import re
import constants


class Parenthesis_remover(object):
    def remove_inside_round_parenthesis(self, text):
        for parentheses in constants.ROUND_PARENTHESIS:
            if parentheses in text:
                pattern_1 = re.compile('（(.*?)）')
                pattern_2 = re.compile('\(.*?\)')
                text = pattern_1.sub(text, '')
                text = pattern_2.sub(text, '')
        return text

    def remove_parenthesis(self, text):
        for parentheses in constants.PARENTHESIS:
            text = text.replace(parentheses, '')
        return text

    def remove_all_parenthesis(self, text):
        for parentheses in constants.ALL_PARENTHESIS:
            text = text.replace(parentheses, '')
        return text
