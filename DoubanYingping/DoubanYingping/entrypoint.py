from scrapy.cmdline import execute
import os
import time
# execute(['scrapy', 'crawl', 'yingping', '-a', 'start_urls=https://movie.douban.com/subject/1296141/'])

if __name__ == "__main__":
    os.system('scrapy crawl getfilmurls')
    # time.sleep(2)
    # with open('./urls.txt', 'r') as f:
    #     url = f.readline()
    #     print(url)
    #     os.system('scrapy crawl yingping -a start_urls='+url.strip())