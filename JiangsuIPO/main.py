import requests, json, hashlib, tpolicy, time, os, chardet
from bs4 import BeautifulSoup
from urllib import parse

def get_hash(url):
    filename = hashlib.md5()
    filename.update(url.encode("utf8"))
    return filename.hexdigest()

def RootUrlConstructor(root, pages):
    l = [parse.urljoin(root, "index.html")]
    for i in range(pages)[1:]:
        l.append(parse.urljoin(root, "index_%s.html" % i))
    return l

folders = ["Atta", "Data", "Json", "SQL"]
for f in folders:
    if not os.path.exists(f):
        os.makedirs(f)

btime = time.time()

RootUrl = [('http://www.jsip.gov.cn/tzgg/', 25),
           ('http://www.jsip.gov.cn/zwgk/gfwj/xgzc/', 8),
           ('http://www.jsip.gov.cn/zwgk/ghjh/zlgh/', 1)]

UrlList = []
for u in RootUrl:
    UrlList.extend(RootUrlConstructor(u[0], u[1]))

n = 0


DictList = []
for u in UrlList:
    r = requests.get(u)
    b = BeautifulSoup(r.content, "html.parser")
    t = b.find("div", class_="col-list")
    for i in t.find_all("li"):
        d = {}
        d["title"] = i.a.find("div", class_="text").get_text()
        d["publish_date"] = i.a.find("div", class_="text-date").get_text()
        d["orig_url"] = parse.urljoin(u, i.a["href"])
        if get_hash(d["orig_url"]) in os.listdir("Json/"):
            n += 1
            print("已采集！", n)
            continue
        if d["orig_url"].split(".")[-1] != "html":
            d["content"] = '<p><a href="{0}">{1}</a></p>'.format(d["orig_url"], d["title"])
            print(d)
        else:
            policypage = requests.get(d["orig_url"])
            policypageb = BeautifulSoup(policypage.content, "html.parser")
            d['content'] = str(policypageb.find("div", style="clear:both;text-align:left;"))
        with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
        print(round(time.time() - btime, 3))


# r = requests.get(RootUrl[0])
# b = BeautifulSoup(r.content, "html.parser")
# print(b.find("a", text="下一页"))