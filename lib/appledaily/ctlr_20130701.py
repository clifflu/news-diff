from .. import Ctlr_base_RSS

class Ctlr(Ctlr_base_RSS):
  _rss_urls = [
    "http://www.appledaily.com.tw/rss/create/kind/sec/type/1077"
  ]

  def parse_article(self, payload):
    print(list(payload))
    return {'asdf': 'ghij'}