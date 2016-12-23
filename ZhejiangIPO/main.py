import requests, json, hashlib, tpolicy, time, os, chardet, re
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

def get_json(b):
    pass

folders = ["Atta", "Data", "Json", "SQL"]
for f in folders:
    if not os.path.exists(f):
        os.makedirs(f)

btime = time.time()

RootUrl = "http://www.zjpat.gov.cn/interIndex.do?method=list22&curPage=1&dir=/zjszscqj/tzgg"
# RootUrl = "http://www.zjpat.gov.cn/interIndex.do?method=list22&curPage=51&dir=/zjszscqj/tzgg"
r = requests.get(RootUrl)
b = BeautifulSoup(r.content, "html.parser")
# 提取正文
for x in b.find("table", class_="mgt03").find_all("tr"):
    # print(x)
    d = {}
    d['title'] = x.a["title"].strip()
    d['publish_date'] = x.find("td", width="19%").get_text().strip()[1:-1]
    d['orig_url'] = parse.urljoin(RootUrl, x.a["href"])
    pager = requests.get(d['orig_url'])
    pageb = BeautifulSoup(pager.content, "html.parser")
    d['content'] = ''.join([str(j) for j in pageb.find_all("p", class_="MsoNormal")])
    attar = requests.get(parse.urljoin(RootUrl,pageb.find("iframe")["src"]))
    attab = BeautifulSoup(attar.content, "html.parser")
    if attab.find_all("a"):
        attacontent = '<p>附件：</p>'
        attacontent += ''.join(['<p>' + str(j) + '</p>' for j in attab.find_all("a")])
        d['content'] += attacontent
    # print('\n'.join([str(j) for j in attab.find_all("a")]))
    if d['content'] == '':
        if pageb.find("td", class_="fs14p"):
            print("有fs14p")
        else:
            print("无fs14p，请检查%s" % d['orig_url'])
    with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
        f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
    print(round(time.time() - btime, 3))

# 检测下一页
while b.find("a", text=re.compile("下一页")):
    NextUrl = parse.urljoin(RootUrl, b.find("a", text=re.compile("下一页"))['href'])
    r = requests.get(NextUrl)
    b = BeautifulSoup(r.content, "html.parser")
    # 提取正文
    for x in b.find("table", class_="mgt03").find_all("tr"):
        # print(x)
        d = {}
        d['title'] = x.a["title"].strip()
        d['publish_date'] = x.find("td", width="19%").get_text().strip()[1:-1]
        d['orig_url'] = parse.urljoin(NextUrl, x.a["href"])
        pager = requests.get(d['orig_url'])
        pageb = BeautifulSoup(pager.content, "html.parser")
        d['content'] = ''.join([str(j) for j in pageb.find_all("p", class_="MsoNormal")])
        if pageb.find("iframe"):
            attar = requests.get(parse.urljoin(NextUrl, pageb.find("iframe")["src"]))
            attab = BeautifulSoup(attar.content, "html.parser")
            if attab.find_all("a"):
                attacontent = '<p>附件：</p>'
                attacontent += ''.join(['<p>' + str(j) + '</p>' for j in attab.find_all("a")])
                d['content'] += attacontent
        # print('\n'.join([str(j) for j in attab.find_all("a")]))
        if d['content'] == '':
            if pageb.find("td", class_="fs14p"):
                print("有fs14p")
                print(pageb.find("td", class_="fs14p"))
                d['content'] = str(pageb.find("td", class_="fs14p"))
            else:
                print("无fs14p，请检查%s" % d['orig_url'])
        with open("Json/" + get_hash(d["orig_url"]), 'w', encoding="utf8") as f:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4))
        print(round(time.time() - btime, 3))
#     NextUrl = parse.urljoin(RootUrl, b.find("a", text=re.compile("下一页"))["href"])
#     print(NextUrl)
#     r = requests.get(NextUrl)
#     b = BeautifulSoup(r.content, "html.parser")
#     get_json(b)