import requests, json, hashlib, tpolicy, time
from bs4 import BeautifulSoup
from urllib import parse

def RootUrlConstructor(root, pages):
    l = [parse.urljoin(root, "index.html")]
    for i in range(pages)[1:]:
        l.append(parse.urljoin(root, "index_%s.html" % i))
    return l

def get_hash(url):
    filename = hashlib.md5()
    filename.update(url.encode("utf8"))
    return filename.hexdigest()

btime = time.time()

RootUrl = [('http://www.hnipo.gov.cn/xxgk/tzgg/', 40),
           # 'http://www.hnipo.gov.cn/xxgk/yjgl/',
           ('http://www.hnipo.gov.cn/xxgk/zcfg/', 7)]

UrlList = []
for u in RootUrl:
    UrlList.extend(RootUrlConstructor(u[0], u[1]))

DictList = []
for u in UrlList:
    r = requests.get(u)
    b = BeautifulSoup(r.content, "html.parser")
    t = b.find("table", class_="table_list")
    for i in t.tbody.find_all("tr"):
        d = {}
        d["publish_date"] = i.find_all("td")[2].get_text()
        d["orig_url"] = parse.urljoin(u, i.find_all("td")[1].a["href"])
        policypage = requests.get(d["orig_url"])
        policypageb = BeautifulSoup(policypage.content, "html.parser")
        d['title'] = policypageb.find("div", class_="main_content").h2.get_text()
        d['content'] = str(policypageb.find("div", class_="main_con_zw"))
        with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
        print(round(time.time() - btime, 3))



