# -*- coding: utf-8 -*-
import re
import constants
import sre_constants


class Parenthesis_remover(object):
    def remove_inside_round_parenthesis(self, text):
        for parentheses in constants.ROUND_PARENTHESIS:
            if parentheses in text:
                pattern_1 = re.compile('（(.*?)）')
                pattern_2 = re.compile('\(.*?\)')
                try:
                    text = pattern_1.sub(text, '')
                    text = pattern_2.sub(text, '')
                except sre_constants.error:
                    continue
        return text

    def remove_parenthesis(self, text):
        for parentheses in constants.PARENTHESIS:
            text = text.replace(parentheses, '')
        return text

    def remove_all_parenthesis(self, text):
        for parentheses in constants.ALL_PARENTHESIS:
            text = text.replace(parentheses, '')
        return text
