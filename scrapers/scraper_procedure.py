import json
import re
import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse
from queue import deque
from scraper_diagnosis import Scraper, levelFactory, startendExtractorFactory, singleExtractorFactory


if __name__ == '__main__':
    regex1 = '^(\d+\.\s*)?(?P<descr>[\-\d\w\s\,\.]*)\s*\((?P<start>\w?\d+)(-(?P<end>\w?\d+)\))?'
    regex2 = '^\s*(?P<code>\w?\d+(\.\d*)?)\s+(?P<descr>.*)'
    l1links = levelFactory('.lvl1', 'div.chapter', startendExtractorFactory(regex1))
    l2links = levelFactory('.lvl2', 'div.dlvl', singleExtractorFactory(regex2))
    l3links = levelFactory('.lvl3', 'div.dlvl', singleExtractorFactory(regex2))
    l4links = levelFactory('.lvl4', 'div.dlvl', singleExtractorFactory(regex2))
    handlers = [l1links, l2links, l3links, l4links]
    scraper = Scraper(handlers)
    scraper.push(0, 'http://icd9cm.chrisendres.com/index.php?action=procslist')
    
    
    hierarchies = scraper.run()
    
    with open('./codes_procedure.json','w') as f:
        codes = [x for x in hierarchies]
        f.write(json.dumps(codes))