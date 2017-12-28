# -*- coding: utf-8 -*-

# Scrapy settings for Taonvlang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Taonvlang'

SPIDER_MODULES = ['Taonvlang.spiders']
NEWSPIDER_MODULE = 'Taonvlang.spiders'

MONGO_URI='localhost'
MONGO_DB='taonvlang'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Taonvlang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'cookie':'tracknick=tb4192332_2012; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; UM_distinctid=15dbfe52514207-04b2f5bc0dad73-5c6a3a7a-100200-15dbfe52516189; miid=1819893462062305719; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; CNZZDATA30063598=cnzz_eid%3D1240630502-1506404882-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1506410623; mt=ci%3D-1_0; v=0; cookie2=1f2c6d580c0f148fbc23e44a72de8f8f; t=161b12068ebd1c81ad307468bd85c61c; _tb_token_=51e38b59445f8; CNZZDATA30064598=cnzz_eid%3D1465862291-1506410103-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1506497588; CNZZDATA30063600=cnzz_eid%3D657822935-1506407601-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1506497588; cna=KHPKEQF/owQCAd5P091TEN2z; isg=AqWlkF1UEG9PMHRxJxBdyAqptGGxCilIDLs31KeKYVzrvsUwbzJpRDNePhQz; JSESSIONID=94615D4E06F9128BD591C9C4B3A69B13; uc1=cookie14=UoTcCfQsoQo68g%3D%3D'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Taonvlang.middlewares.TaonvlangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Taonvlang.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Taonvlang.pipelines.MyImagesPipeline':1,
   'Taonvlang.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

IMAGES_STORE='E:\python\Pycharm\Taonvlang'
IMAGES_EXPIRES=90

IMAGES_THUMBS={
    'small':(50,50),
    'big':(200,200),
}