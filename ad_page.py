from web_page import WebPage


class AdPage(WebPage):
    def set_ads_with_html_body(self):
        listWrap = pq(self.html_body).find('.listWrap')
        lis = listWrap.children().children()
        self.ads = []
        for li in lis:
            pq_li = pq(li)
            title = pq_li.find('a').text()
            link = pq_li.find('a').attr('href')
            snippet = pq_li.find('.smr').text()
            ad_info = {'title': title, 'snippet': snippet, 'link': link}
            ad = Ad(ad_info)
            self.ads.append(ad)

