import constants
import time
from ad_fetcher import AdFetcher
from pickle_file_saver_for_ads import PickleFileSaverForAds

if __name__ == '__main__':
    for query in constants.QUERIES_1:
        ad_fetcher = AdFetcher(query)
        ads = ad_fetcher.fetch_ads()
        pfs = PickleFileSaverForAds()
        pfs.save_ads_with_query(ads=ads, query=query)
        time.sleep(1)
