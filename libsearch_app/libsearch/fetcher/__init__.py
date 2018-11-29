from .processing.zip import ZIPParser

def apk_downloader(category):
    for page in range(1,100):
        page = requests.get('https://apkpure.com/%s?sort=new&page=%d' % (category, page))
        tree = html.fromstring(page.content)
        links = tree.xpath('//ul[@id="pagedata"]/li/div[@class="category-template-down"]/a')
        for link in links:

            page = requests.get('https://apkpure.com%s' % link.get("href"))
            tree = html.fromstring(page.content)
            download_link = tree.xpath('//a[@id="download_link"]')[0]
            name = tree.xpath('//div[@class="fast-download-box"]//span[@class="file"]/text()')[0].strip()
            name = re.sub('[^\w\-_\. ]', '_', name)

            try:
                if not os.path.isfile("./cache/%s" % name):
                    page = requests.get(download_link.get("href"), allow_redirects=True)
                    open('./cache/%s' % name, 'wb').write(page.content)
                    ZIPParser().parse(name)
                    print "Downloaded %s" % name
            except:
                print "Failed downloading %s" % name 
