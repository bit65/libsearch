import requests
from lxml import html
import os
import shutil
from libsearch.storage.indexer import Indexer
from libsearch.processing.base import ParserBase
from libsearch.processing.searchparser import Parser
import zipfile


try:
    os.mkdir('./cache')
except:
    pass
try:
    os.mkdir('./res')
except:
    pass

# parser = etree.XMLParser(recover=True)
def apk_downloader(link, s=None, download=True):
    host = "https://apkpure.com"

    apk_data = {}
    if s is None:
        s = requests.session()

    apk_class= link.split('/')[-1]
    
    apk_data['pkg'] = apk_class

    if not os.path.isfile("./cache/%s" % apk_class):
        try:
            page = s.get('%s%s' % (host, link), verify=False)
            tree = html.fromstring(page.content)            

            # Get image data
            # img_link = tree.xpath('//div[@class=\'icon\']/img[1]')[0]
            # page = s.get(img_link.get('src'), allow_redirects=True, stream=True, verify=False)
            # with open('./res/%s' % apk_class + '.png', 'wb') as f:
            #     shutil.copyfileobj(page.raw, f)
            
            # base = ParserBase(apk_class + '.apk')

            # Get APK data
            # apk_data['name'] = tree.xpath('//div[@class=\'title-like\']/h1[1]')[0].text
            # apk_data['version'] = tree.xpath('//div[@class=\'details-sdk\']/span[1]')[0].text
            # apk_data['tags'] = [t.text for t in  tree.xpath('//ul[@class=\'tag_list\']/li/a[1]')]
            # apk_data['categories'] = [c.text for c in  tree.xpath('//p[2]/a[1]/span')]

            # Indexer.instance().save(base.createData("meta","apkinfo", **apk_data))


            # Get Download
            print "* downloading %s" % apk_class
            page = s.get('%s%s/download?from=details' % (host, link), verify=False)
            tree = html.fromstring(page.content)            
            download_link = tree.xpath('//iframe[@id=\'iframe_download\']')[0]

            if download == False:
                return download_link.get('src')
            # fpin = NetZip(download_link.get('src'))
            # print zipfile._EndRecData(fpin)
            # exit(0)

            # if length < 80000000:
            with open('./cache/%s.apk' % apk_class, 'wb') as f:
                shutil.copyfileobj(page.raw, f)
            
            # parser = Parser.instance().get_parser('./cache/%s.apk' % apk_class)
            # if parser != None:
            # 	parser.parse(save=True)

            
        except Exception as e:
            print "Failed downloading %s" % apk_class
            import traceback
            print(traceback.format_exc())

    return apk_data

def apk_search(search):
    apk_data = []

    if isinstance(search, list):
        for d in search:
            apk_data.append(apk_downloader(d))
        return apk_data
        
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
            apk_data.append(apk_downloader(link, s))

    return apk_data
