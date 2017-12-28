# -*- coding: utf-8 -*-

# Scrapy settings for toutiao_chanfu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'toutiao_chanfu'

SPIDER_MODULES = ['toutiao_chanfu.spiders']
NEWSPIDER_MODULE = 'toutiao_chanfu.spiders'

MONGO_URI='localhost'
MONGO_DB='chanfuissue'

HTTPERROR_ALLOWED_CODES = [400]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'toutiao_chanfu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': '*/*',
  'Accept-Language': 'zh-Hans;q=1, en;q=0.9, zh-Hant;q=0.8, fr;q=0.7, de;q=0.6, ja;q=0.5',
  'Host: ic.snssdk.com'
  'Proxy-Connection':'keep-alive',
  'Cookie':'CNZZDATA1263676333=1053471997-1506224751-%7C1506224751; install_id=15419404350; qh[360]=1; ttreq=1$81cf78bc9e126dbc3f1e1a22789fdc99f9039157; UM_distinctid=15eb20c9b0da-0f7a55db4-3d5b614e-25800-15eb20c9b102e',
  'X-SS-Cookie':'CNZZDATA1263676333=1053471997-1506224751-%7C1506224751; install_id=15419404350; qh[360]=1; ttreq=1$81cf78bc9e126dbc3f1e1a22789fdc99f9039157; UM_distinctid=15eb20c9b0da-0f7a55db4-3d5b614e-25800-15eb20c9b102e',
  'Connection':'keep-alive',
  'User-Agent':'News/6.3.4 (iPhone; iOS 7.0.3; Scale/2.00)',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'toutiao_chanfu.middlewares.ToutiaoChanfuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'toutiao_chanfu.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'toutiao_chanfu.pipelines.MongoPipeline': 200,
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
