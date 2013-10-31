from web_item import WebItem
import re

class TaskStep(WebItem):
    def set_headings_from_text(self, text):
        self.set_step_text(text)
        self.set_h2()
        self.set_h3s()

    def set_h2(self):
        index_for_the_end_of_h2 = self.step_text.find('</h2>')
        self.h2 = self.step_text[:index_for_the_end_of_h2].strip()

    def set_h3s(self):
        h3_pattern = re.compile('<h3>.*?</h3>')
        h3s = h3_pattern.findall(self.step_text)
        stripped_h3s = []
        for h3 in h3s:
            stripped_h3s.append(h3[5:-5].strip())
        self.h3s = stripped_h3s

    def set_step_text(self, text):
        self.step_text = text
