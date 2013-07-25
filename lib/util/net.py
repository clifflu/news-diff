# -*- encoding: utf-8 -*-
#

import urllib

portal_ptrn_list = {
  'feedsportal': "\.feedsportal\.com",
}

def get_portal(url):
  import re

  for portal in portal_ptrn_list:
    ptrn = re.compile(portal_ptrn_list[portal])
    if (ptrn.search(url)): return portal

  return False

def break_portal(portal, payload, uo):
  try:
    if 'feedsportal' == portal:
      return _break_portal_feedsportal(payload, uo)
  except Exception:
    import traceback
    print('\n***\nBreak Portal Failed (%s, %s) ***' % (portal, payload['url']))
    traceback.print_exc()

def _break_portal_feedsportal(payload, uo):
  from lxml.html import fromstring

  text = uo.read()
  try:
    html = fromstring(text)
    payload['url_read'] = html.cssselect('a')[0].attrib['href']
    payload['response'] = urllib.urlopen(payload['url_read'])
  except:
    payload['url_read'] = uo.url
    payload['response'] = text

def fetch(payload, dbi = None):
  """抓取 payload['url'] 的檔案
  並將最終讀取到的 url 寫入 payload['url_read'], response 寫入 payload['response']
  """
  import re
  from lxml.html import fromstring

  from lib import db, DB
  from lib.util.text import to_unicode

  if dbi is None: _dbi = DB()
  else: _dbi = dbi

  try:
    uo = urllib.urlopen(payload['url'])

    portal = get_portal(uo.url)
    if portal:
      break_portal(portal, payload, uo)
    else:
      payload['response'] = uo.read()
      payload['url_read'] = uo.url

  except Exception as e:
    payload['response'] = 'error ' + unicode(e)
    payload['category'] = 'error'

  if 'url_read' not in payload:
    payload['url_read'] = payload['url']

  db.save_fetch(payload['url'], to_unicode(payload['response']), payload['category'], dbi = _dbi)
  del payload['category'] # consumed here

  if dbi is None: _dbi.disconnect()

  return payload

def normalize_url(url):
  import re
  url = url.rstrip('/')
  return re.sub('^https?://', '', url)
