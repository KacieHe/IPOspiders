import requests, json, hashlib, tpolicy, time, os, chardet
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

RootUrl = "http://www.ahipo.gov.cn/sm2111111188.asp"

r = requests.get(RootUrl)
b = BeautifulSoup(r.content, "html.parser")
NextPage = RootUrl
while b.find("a", text="下一页 "):
    d = {}
    list_news = b.find("ul", class_="list_news")
    for i in list_news.find_all("li"):
        d["orig_url"] = parse.urljoin(NextPage, i.a["href"])
        d['title'] = i.a["title"]
        d["publish_date"] = i.span.get_text().replace("/", "-")
        page = requests.get(d["orig_url"])
        try:
            pageb = BeautifulSoup(page.content.decode("GB2312"), "html.parser")
            # pageb = BeautifulSoup(page.content, "html.parser")
        except:
            try:
                pageb = BeautifulSoup(page.content.decode("utf8"), "html.parser")
            except:
                print(chardet.detect(page.content))
                print(d["orig_url"], d['title'])
        content = pageb.find("div", class_="content_nr")
        if content:
            deltag = content.find("div", class_="close")
        else:
            deltag = False
        if deltag:
            deltag.extract()
        d["content"] = str(content)
        with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
        print(round(time.time() - btime, 3))
    NextPage = parse.urljoin(RootUrl, b.find("a", text="下一页 ")["href"])
    r = requests.get(NextPage)
    b = BeautifulSoup(r.content, "html.parser")