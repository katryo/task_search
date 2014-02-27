# -*- coding: utf-8 -*-
import constants
import pdb
from pickle_file_saver_for_original import PickleFileSaverForOriginal
from page_data_loader import PageDataLoader
from web_page import WebPage

if __name__ == '__main__':
    queries = constants.QUERIES_4
    saver = PickleFileSaverForOriginal()
    with PageDataLoader() as page_loader:
        for query in queries:
            pages = []
            page_ids = page_loader.page_ids_with_query(query)
            for page_id in page_ids:
                pagedata = page_loader.pagedata_with_id(page_id)  # (id, url, snippet, body, rank)
                page = WebPage(id=page_id,
                               url=pagedata[0],
                               query=pagedata[1],
                               snippet=pagedata[2],
                               rank=pagedata[3])
                pages.append(page)
            saver.save_pages_with_query(pages=pages, query=query)

