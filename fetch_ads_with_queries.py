import constants
import time
from ad_fetcher import AdFetcher
from pickle_file_saver import PickleFileSaver

if __name__ == '__main__':
    for query in constants.QUERIES:
        ad_fetcher = AdFetcher(query)
        ads = ad_fetcher.fetch_ads()
        pfs = PickleFileSaver()
        pfs.save_ads_with_query(ads=ads, query=query)
        time.sleep(1)
