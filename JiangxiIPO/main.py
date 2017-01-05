import requests, json, hashlib, tpolicy, time, os, chardet, re
from bs4 import BeautifulSoup
from urllib import parse

def get_hash(url):
    filename = hashlib.md5()
    filename.update(url.encode("utf8"))
    return filename.hexdigest()

folders = ["Atta", "Data", "Json", "SQL"]
for f in folders:
    if not os.path.exists(f):
        os.makedirs(f)

btime = time.time()

def get_policy(b):
    right_news = b.find("div", class_="right_news")
    for i in right_news.find_all("li"):
        d = {'publish_date': i.span.get_text(), 'orig_url': parse.urljoin(RootUrl, i.a['href'])}
        pager = requests.get(d['orig_url'])
        pageb = BeautifulSoup(pager.content, "html.parser")
        d['title'] = pageb.find("div", class_="title").h3.get_text()
        d['content'] = str(pageb.find("div", class_="neino"))
        with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
        print(round(time.time() - btime, 3))


RootUrl = "http://www.jxipo.gov.cn/list/15.aspx"

r = requests.get(RootUrl)
b = BeautifulSoup(r.content, "html.parser")
get_policy(b)
NextUrl = parse.urljoin(RootUrl, b.find("a", text=re.compile("下一页"))['href'])
while NextUrl != "javascript:;":
    r = requests.get(NextUrl)
    b = BeautifulSoup(r.content, "html.parser")
    get_policy(b)
    NextUrl = parse.urljoin(RootUrl, b.find("a", text=re.compile("下一页"))['href'])
    print(NextUrl)
