import requests
from lxml import html
import os
import code

host = "https://apkpure.com"
# parser = etree.XMLParser(recover=True)

def apk_downloader(search):
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
            apk_class= link.split('/')[-1] + '.apk'

            if not os.path.isfile("./cache/%s" % apk_class):
                try:
                    page = s.get('%s%s/download?from=details' % (host, link))
                    tree = html.fromstring(page.content)
                    # apk_class= tree.xpath('//@data-pkg')[0] + '.apk'
                    download_link = tree.xpath('//iframe[@id=\'iframe_download\']')[0]
                    
                    page = s.get(download_link.get('src'), allow_redirects=True)
                    open('./cache/%s' % apk_class, 'wb').write(page.content)
                    print "Downloaded %s" % apk_class
                except Exception as e:
                    print "Failed downloading %s" % apk_class
                    print e
