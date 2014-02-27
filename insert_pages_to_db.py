# -*- coding: utf-8 -*-
import pdb
from pickle_file_loader_for_original import PickleFileLoaderForOriginal
from page_data_inserter import PageDataInserter
import constants


if __name__ == '__main__':
    original_queries = constants.QUERIES_4
    pfl = PickleFileLoaderForOriginal()
    with PageDataInserter() as di:
        for query in original_queries:
            pages = pfl.load_fetched_pages_with_query(query)
            for page in pages:
                if not '.pdf' in page.url:
                    if not di.has(page.query, page.url):
                        di.insert(
                            page.query,
                            page.url,
                            page.title.replace('"', ''),
                            page.snippet.replace('"', ''),
                            page.rank
                        )

