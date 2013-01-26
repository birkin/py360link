# -*- coding: utf-8 -*-
import os
try:
    import json
except ImportError:
    import simplejson as json
import unittest
from pprint import pprint

from py360link.link360 import Response, Item

#Directory where test data is stored.  
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data')

def read_data(filename):
    path = os.path.join(DATA_PATH, filename)
    content = open(path)
    return content

class TestAPIResponse(unittest.TestCase):
    def setUp(self):
        self.api_resp = read_data('article.xml')
        self.resp = Response(self.api_resp)
        self.bib = self.resp.results()[0]

    def test_result_length(self):
        results = self.resp.results()
        self.assertEqual(len(results), 1)

    def test_query(self):
        query = self.resp.query
        self.assertEqual(query, 
                        'version=1.0&url_ver=Z39.88-2004&id=pmid:19282400&sid=Entrez:PubMed')

    def test_library(self):
        lib = self.resp.library
        self.assertEqual(lib, 'Your University')

    def test_library_id(self):
        code = self.resp.library_id
        #self.assertEqual(code, '1234')


class TestArticleResponse(unittest.TestCase):

    def setUp(self):
        self.api_resp = read_data('article.xml')
        self.resp = Response(self.api_resp)
        self.bib = self.resp.results()[0]

    def test_format(self):
        self.assertEqual(self.bib.format, 'journal')

    def test_btype(self):
        self.assertEqual(self.bib.btype, 'article')

    def test_links(self):
        links = self.bib.get_links()
        for link in links:
            if link['type'] == 'article':
                self.assertEqual(link['anchor'], 'Full text available from SAGE Premier 2008.')
            elif link['type'] == 'journal':
                self.assertEqual(link['coverage_start'],  '2007-02-01')

    def test_meta(self):
        meta = self.bib.meta()
        #pprint(meta)
        self.assertEqual(meta['doi'], '10.1177/1753193408098482')
        self.assertEqual(meta['pmid'], '19282400')
        self.assertEqual(meta.get('isbn'), None)

class TestBookChapterResponse(unittest.TestCase):

    def setUp(self):
        self.api_resp = read_data('bookchapter_not_held.xml')
        self.resp = Response(self.api_resp)
        self.bib = self.resp.results()[0]

    def test_format(self):
        self.assertEqual(self.bib.format, 'book')

    def test_btype(self):
        self.assertEqual(self.bib.btype, 'inbook')

    def test_links(self):
        self.assertEqual(self.bib.get_links(), None)

    def test_meta(self):
        meta = self.bib.meta()
        self.assertEqual(meta.get('title'), 'New methods for the analysis of change.')
        self.assertEqual(meta.get('doi'), '10.1037/10409-006')
        self.assertTrue(('isbn', '9781557987549') in meta.get('isn'))



class TestLinkSort(unittest.TestCase):

    def test_known_dbs(self):
        """
        [{'url': 'http://revproxy.brown.edu/login?url=http://online.sagepub.com/', 'coverage_start': '2007-02-01', 'type': 'source', 'anchor': 'SAGE Publications', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://jhs.sagepub.com/cgi/doi/10.1177/1753193408098482', 'coverage_start': '2007-02-01', 'type': 'article', 'anchor': 'Full text available from SAGE Premier 2008.', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://online.sagepub.com/1753-1934', 'coverage_start': '2007-02-01', 'type': 'journal', 'anchor': 'Journal website', 'provider': 'SAGE Publications'}, {'url': 'http://revproxy.brown.edu/login?url=http://jhs.sagepub.com/content/vol34/issue2/', 'coverage_start': '2007-02-01', 'type': 'issue', 'anchor': 'Browse this issue', 'provider': 'SAGE Publications'}]
        """
        pass

class TestLookups(unittest.TestCase):

    def test_lookup(self):
        return
        from py360link import get
        query = 'rft_id=info:doi/10.1016/j.neuroimage.2009.12.024'
        key = 'rl3tp7zf5x'
        resp = get(query, key=key)
        
        pprint(resp.json())
        import ipdb; ipdb.set_trace()
        #for result in resp.records:
        #    pprint(resp.bibjson(result))
        #import ipdb; ipdb.set_trace()
        #print resp.json()



def suite():
    suite1 = unittest.makeSuite(TestAPIResponse, 'test')
    suite2 = unittest.makeSuite(TestArticleResponse, 'test')
    suite3 = unittest.makeSuite(TestBookChapterResponse, 'test')
    suite4 = unittest.makeSuite(TestLookups, 'test')
    all_tests = unittest.TestSuite((suite1,suite2, suite3, suite4))
    return all_tests

if __name__ == '__main__':
    unittest.main()
