# encoding: utf-8

import sys
import datetime
import requests
import regex
import lxml.html
import unicodecsv
from collections import namedtuple


docket_url_pattern = regex.compile(ur'^http://archive\.org/details/gov\.uscourts\.(?P<docket_id>.+)$')
DocketHref = namedtuple(u'DocketHref', ['docket_id', 'href'])

docket_dir_url_pattern = regex.compile(ur'https://(.+\.)?archive\.org/[0-9]+/items/gov\.uscourts\.(?P<docket_id>.*+)$')

def fetch_html_document(url):
    response = requests.get(url)
    assert response.status_code == 200
    doc = lxml.html.fromstring(response.text)
    doc.make_links_absolute(url)
    return doc

def fetch_listing(page):
    url_tmpl = u'http://archive.org/search.php?query=collection%3Ausfederalcourts&sort=-publicdate&page={page}'
    url = url_tmpl.format(page=page)
    return fetch_html_document(url)

def extract_docket_urls(doc):
    links = [DocketHref(match.groupdict()[u'docket_id'], match.group())
             for match in [docket_url_pattern.match(href)
                           for href in [a.attrib[u'href'] for a in doc.xpath(u'//a')]]
             if match is not None]
    return links

def extract_docket_dir_url(docket_id, page):
    links = [DocketHref(docket_id, match.group())
             for match in [docket_dir_url_pattern.match(href)
                           for href in [a.attrib[u'href'] for a in page.xpath(u'//a')]]
             if match is not None]
    if len(links) == 0:
        print >> sys.stderr, u"Unable to find docket directory url for docket {docket}".format(docket=docket_id)
        return None
    elif len(links) > 1:
        print >> sys.stder, u"Found multiple ({count}) docket directory urls than expected for docket {docket}".format(count=len(links), docket=docket_id)
        return None
    else:
        return links[0]

def determine_page_count():
    first_listing_url = u'http://archive.org/search.php?query=collection%3Ausfederalcourts&sort=-publicdate'
    doc = fetch_html_document(first_listing_url)
    anchors = doc.xpath('//a[text() = "Last"]')
    assert len(anchors) > 0
    page_pattern = regex.compile(u'page=(?P<pgnum>\d+)')
    match = page_pattern.search(anchors[0].attrib['href'])
    assert match is not None
    assert 'pgnum' in match.groupdict()
    return int(match.groupdict()['pgnum'])

def main():
    page_count = determine_page_count()
    try:
        limit = int(sys.argv[1])
        page_count = min(page_count, limit)
    except:
        pass

    csv = unicodecsv.writer(sys.stdout, [u'docket_id', u'mirror_dir'])

    for pgnum in range(1, page_count + 1):
        print >> sys.stderr, u"Fetching docket listing page {pgnum} of {pgcnt}".format(pgnum=pgnum, pgcnt=page_count)
        listing_page = fetch_listing(pgnum)
        dockets = extract_docket_urls(listing_page)
        for docket in dockets:
            docket_page = fetch_html_document(docket.href)
            docket_dir = extract_docket_dir_url(docket.docket_id, docket_page)
            csv.writerow([docket.docket_id,
                          docket_dir.href])


if __name__ == "__main__":
    main()

