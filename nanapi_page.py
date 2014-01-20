from web_page import WebPage


class NanapiPage(WebPage):
    def find_urls_from_nanapi_search_result(self):
        link_elems = pq(self.html_body.encode('utf-8')).find('.item-title a')
        urls = []
        for link_elem in link_elems:
            url = pq(link_elem).attr('href')
            urls.append(url)
        return urls

    def find_task_from_nanapi_with_headings(self):
        # h2 has_many h3 s
        # self.html_bodyのうち、recipe-bodyを取ってくる
        recipe_body = pq(self.html_body.encode('utf-8')).find('.recipe-body').html()
        # splitして
        steps_texts = recipe_body.split('<h2>')[1:]
        task_steps = []
        for step_text in steps_texts:
            task_step = TaskStep()
            task_step.set_headings_from_text(step_text)
            task_steps.append(task_step)
            # step_text => h2からh2まで
        task = Task()
        task.set_title_with_html(self.html_body)
        task.set_url(self.url)
        task.set_steps(task_steps)
        return task # task.steps => [task_step, task_step, ...]
