import requests
from lxml import html
import os
import code
import shutil

host = "https://apkpure.com"
try:
    os.mkdir('./cache')
except:
    pass
# parser = etree.XMLParser(recover=True)
def apk_downloader(link, s=None):

    if s is None:
        s = requests.session()

    apk_class= link.split('/')[-1] + '.apk'
    if not os.path.isfile("./cache/%s" % apk_class):
        try:
            page = s.get('%s%s/download?from=details' % (host, link))
            tree = html.fromstring(page.content)
            # apk_class= tree.xpath('//@data-pkg')[0] + '.apk'
            download_link = tree.xpath('//iframe[@id=\'iframe_download\']')[0]
            
            page = s.get(download_link.get('src'), allow_redirects=True, stream=True)
            with open('./cache/%s' % apk_class, 'wb') as f:
                shutil.copyfileobj(page.raw, f)
                
            print "Downloaded %s" % apk_class
        except Exception as e:
            print "Failed downloading %s" % apk_class
            print e

def apk_search(search):
    if isinstance(search, list):
        for d in search:
            apk_downloader(d)
        return
        
    # for page in range(1,100):
    pos = 0
    s = requests.session()

    while True:
        page = s.get('%s/search-page?q=%s&begin=%d' % (host, search, pos))
        print '%s/search-page?q=%s&begin=%d' % (host, search, pos)
        tree = html.fromstring(page.content)
        # code.interact(local=locals())
        links = tree.xpath('//dl[@class=\'search-dl\']/dt[1]/a[1]/@href')
        if len(links) == 0:
            break
        print "Found %d" % len(links)
        
        for link in links:
            pos += 1
            apk_downloader(link, s)
