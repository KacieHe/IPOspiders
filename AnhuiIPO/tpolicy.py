import json, time, hashlib, re, os, requests
from bs4 import BeautifulSoup
from urllib import parse

class Policy:
    id = ''  # 1-1000
    catid = ''  # 13
    typeid = '0'  # 0
    title = ''  # 标题
    style = ''  # null
    thumb = ''  # null
    keywords = ''  # null
    description = ''  # 可为空
    posids = '0'  # 0
    url = ''  # eg: /itt/ttpolicy/index.php?m=content&c=index&a=show&catid=13&id=1
    listorder = '0'  # 0
    status = '99'  # 99
    sysadd = '0'  # 0
    islink = '0'  # 0
    username = 'spider'  # consulting
    inputtime = ''  # 1439389764
    updatetime = ''  # 1439389764
    content = ''  # 内容
    publish_date = ''  # 出版日期
    public_no = ''  # 发布号
    meta_policy = ',,'  # 元政策：知识产权战略 知识产权强国
    base_policy = ',,'  # 基本政策：基本政策
    supply_policy = ',,'  # 配套政策：财政政策 金融政策 科技政策 产业政策 贸易政策
    main_policy = ',,'  # 主体相关政策：大学 科研机构 企业 服务业 自然人
    guest_policy = ',,'  # 客体相关政策：专利创造 专利运用 专利保护 专利管理 专利服务
    support_policy = ',,'  # 支持政策：科技创新 企业转型 产业升级 国际贸易 区域发展
    expires_date = '0000-00-00'  # 废除时间
    tags = ''  # null
    passtime = 'null'  # null
    departments = '0'  # 0
    depts = ''  # 颁发部门，需要代码表
    memo = ''  #
    isfront = '0'  # 0
    adminmemo = ''  #
    law_policy = ',,'  # 法律文件：法律 行政法规 部门规章 司法解释 地方法规 地方规章

    ispolicy = True
    orig_url = ''
    hashid = ''

    def __init__(self, d):
        if 'id' in d:
            self.id = d['id']
        else:
            self.id = ''

        if 'catid' in d:
            self.catid = d['catid']
        else:
            self.catid = '0'

        if 'typeid' in d:
            self.typeid = d['typeid']
        else:
            self.typeid = '0'

        if 'title' in d:
            self.title = d['title']
        else:
            self.title = ''

        if 'style' in d:
            self.style = d['style']
        else:
            self.style = ''

        if 'thumb' in d:
            self.thumb = d['thumb']
        else:
            self.thumb = ''

        if 'keywords' in d:
            self.keywords = d['keywords']
        else:
            self.keywords = ''

        if 'description' in d:
            self.description = d['description']
        else:
            self.description = ''

        if 'posids' in d:
            self.posids = d['posids']
        else:
            self.posids = '0'

        # if 'url' in d:
        #     self.url = d['url']
        # else:
        #     self.url = ''
        self.url = ''

        if 'listorder' in d:
            self.listorder = d['listorder']
        else:
            self.listorder = '0'

        if 'status' in d:
            self.status = d['status']
        else:
            self.status = '0'

        if 'sysadd' in d:
            self.sysadd = d['sysadd']
        else:
            self.sysadd = '0'

        if 'islink' in d:
            self.islink = d['islink']
        else:
            self.islink = '0'

        if 'username' in d:
            self.username = d['username']
        else:
            self.username = 'consulting'
        # if 'inputtime' in d:
        #     self.inputtime = d['inputtime']
        # if 'updatetime' in d:
        #     self.updatetime = d['updatetime']
        self.inputtime = int(time.time())
        self.updatetime = int(time.time())

        if 'content' in d:
            if 'orig_url' in d:
                content = '<p><a href="{0}" target="_blank">{0}</ a></ p>'.format(d['orig_url']) + d['content']
            else:
                content = d['content']
            content = '\\n'.join(content.splitlines())
            # print(content)
            # content = content.split('\n')
            # content = '\\n'.join(content)
            # content = content.replace('\n', '<br />')

            content = content.replace("\'", "\"")
            self.content = content
        else:
            self.content = ''

        if 'publish_date' in d:
            self.publish_date = d['publish_date']
        else:
            if 'time' in d:
                self.catch_publish_date(d['time'])
            else:
                self.catch_publish_date('0')

        if 'public_no' in d:
            self.public_no = d['public_no']
        else:
            self.public_no = ''

        if 'meta_policy' in d:
            self.meta_policy = d['meta_policy']
        else:
            self.meta_policy = ',,'

        if 'base_policy' in d:
            self.base_policy = d['base_policy']
        else:
            self.base_policy = ',,'

        if 'supply_policy' in d:
            self.supply_policy = d['supply_policy']
        else:
            self.supply_policy = ',,'

        if 'main_policy' in d:
            self.main_policy = d['main_policy']
        else:
            self.main_policy = ',,'

        if 'guest_policy' in d:
            self.guest_policy = d['guest_policy']
        else:
            self.guest_policy = ',,'

        if 'support_policy' in d:
            self.support_policy = d['support_policy']
        else:
            self.support_policy = ',,'

        if 'expires_date' in d:
            self.expires_date = d['expires_date']
        else:
            self.expires_date = '0000-00-00'

        if 'tags' in d:
            self.tags = d['tags']
        else:
            self.tags = ''

        if 'passtime' in d:
            self.passtime = d['passtime']
        else:
            self.passtime = 'null'

        if 'departments' in d:
            self.departments = d['departments']
        else:
            self.departments = '0'

        if 'depts' in d:
            self.depts = d['depts']
        else:
            self.depts = ''

        if 'memo' in d:
            self.memo = d['memo']
        else:
            self.memo = ''

        if 'isfront' in d:
            self.isfront = d['isfront']
        else:
            self.isfront = '0'

        if 'adminmemo' in d:
            self.adminmemo = d['adminmemo']
        else:
            self.adminmemo = ''

        if 'law_policy' in d:
            self.law_policy = d['law_policy']
        else:
            self.law_policy = ',,'

        if 'ispolicy' in d:
            self.ispolicy = d['ispolicy']
        else:
            self.ispolicy = True

        if 'orig_url' in d:
            self.orig_url = d['orig_url']
        else:
            self.orig_url = ''

        if 'hashid' in d:
            self.hashid = d['url_hash']
        else:
            hashtag = hashlib.md5()
            hashtag.update(self.orig_url.encode("utf8"))
            self.hashid = hashtag.hexdigest()

    def tag(self):
        if self.have_tag() or self.have_saved(): # 逻辑需要修改：已tag-重新save-输出sql；已save-读取save-输出sql
            return True
        print(self.title)
        c = BeautifulSoup(self.content, "html.parser").get_text()
        print(c.strip()[:200], c.strip()[-200:])

        ### 匹配规则 ###
        if "征集公告" in self.title or "公示" in self.title or "公开征集" in self.title \
                or "评审结果公告" in self.title or "笔试" in self.title or "面试" in self.title or '公开招' in self.title\
                or "录用公务员" in self.title or "征集" in self.title or '培训班' in self.title:
            self.ispolicy = False
            self.save()
            return True

        # if "专利示范单位" in self.title:
        #     self.main_policy = ',大学,科研机构,企业,服务业,'
        #     self.save()
        #     return True

        ################
        i = ''
        with open("tactics.txt", "r", encoding="utf8") as f:
            tactics = [x[:-1].split('\t') for x in f.readlines()]

        for t in tactics:
            have_tac = True
            for ti in t[0].split(' '):
                if ti not in self.title:
                    have_tac = False
                    break
            if have_tac:
                i = t[1]

        # if "专利奖" in self.title:
        #     i = "51 52 53 54 55 61"
        if not i:
            i = input("""法律文件:::		11.法律; 12.行政法规; 13.部门规章; 14.司法解释; 15.地方法规; 16.地方规章
元政策:::		21.知识产权战略; 22.知识产权强国
基本政策:::		31.
配套政策:::		41.财政政策; 42.金融政策; 43.科技政策; 44.产业政策; 45.贸易政策
主体相关政策:::	51.大学; 52.科研机构; 53.企业; 54.服务业; 55.自然人
客体相关政策:::	61.专利创造; 62.专利运用; 63.专利保护; 64.专利管理; 65.专利服务
支持政策:::		71.科技创新; 72.企业转型; 73.产业升级; 74.国际贸易; 75.区域发展
""")
        if i == 'f' or i == 'F':
            self.ispolicy = False
            self.save()
            return True

        for x in i.strip().split(' '):
            if x[0] == '1':
                self.law_policy = ','
                if x[1] == '1':
                    self.law_policy += "法律,"
                if x[1] == '2':
                    self.law_policy += "行政法规,"
                if x[1] == '3':
                    self.law_policy += "部门规章,"
                if x[1] == '4':
                    self.law_policy += "司法解释,"
                if x[1] == '5':
                    self.law_policy += "地方法规,"
                if x[1] == '6':
                    self.law_policy += "地方规章,"
            if x[0] == '2':
                self.meta_policy = ','
                if x[1] == '1':
                    self.meta_policy += "知识产权战略,"
                if x[1] == '2':
                    self.meta_policy += "知识产权强国,"
            if x[0] == '3':
                self.base_policy = ',基本政策,'
            if x[0] == '4':
                self.supply_policy = ','
                if x[1] == '1':
                    self.supply_policy += "财政政策,"
                if x[1] == '2':
                    self.supply_policy += "金融政策,"
                if x[1] == '3':
                    self.supply_policy += "科技政策,"
                if x[1] == '4':
                    self.supply_policy += "产业政策,"
                if x[1] == '5':
                    self.supply_policy += "贸易政策,"
            if x[0] == '5':
                self.main_policy = ','
                if x[1] == '1':
                    self.main_policy += "大学,"
                if x[1] == '2':
                    self.main_policy += "科研机构,"
                if x[1] == '3':
                    self.main_policy += "企业,"
                if x[1] == '4':
                    self.main_policy += "服务业,"
                if x[1] == '5':
                    self.main_policy += "自然人,"
            if x[0] == '6':
                self.guest_policy = ','
                if x[1] == '1':
                    self.guest_policy += "专利创造,"
                if x[1] == '2':
                    self.guest_policy += "专利运用,"
                if x[1] == '3':
                    self.guest_policy += "专利保护,"
                if x[1] == '4':
                    self.guest_policy += "专利管理,"
                if x[1] == '5':
                    self.guest_policy += "专利服务,"
            if x[0] == '7':
                self.support_policy = ','
                if x[1] == '1':
                    self.support_policy += "科技创新,"
                if x[1] == '2':
                    self.support_policy += "企业转型,"
                if x[1] == '3':
                    self.support_policy += "产业升级,"
                if x[1] == '4':
                    self.support_policy += "国际贸易,"
                if x[1] == '5':
                    self.support_policy += "区域发展,"

        self.save()

    def have_tag(self):
        if self.meta_policy == ',,' and self.base_policy == ',,' and self.supply_policy == ',,' and self.main_policy == ',,' and self.guest_policy == ',,' and self.support_policy == ',,' and self.law_policy == ',,':
            return False
        else:
            return True

    def save(self):
        filename = hashlib.md5()
        filename.update(self.title.encode("utf8"))
        with open('Data/' + filename.hexdigest(), 'w', encoding="utf8") as f:
            f.write(json.dumps(self.__dict__, ensure_ascii=False, sort_keys=True, indent=4))

    def catch_publish_date(self, time): # 有问题，需要检查
        # print("开始捕捉出版日期")
        f2h = {'１':'1', '２':'2', '３':'3', '４':'4', '５':'5', '６':'6', '７':'7', '８':'8', '９':'9', '０':'0'}
        c = BeautifulSoup(self.content, "html.parser").get_text()
        r = re.compile(r"\d+年\d+月\d+日")
        if not r.findall(c):
            # print("没有找到出版日期")
            if r.findall(time):
                m = re.search(r"(\d+)年(\d+)月(\d+)日", r.findall(time)[-1])

                datestring = ['', '', '']
                for x in [0, 1, 2]:
                    for i in m.group(x + 1):
                        if i in f2h:
                            datestring[x] += f2h[i]
                        else:
                            datestring[x] += i
                for i in [1, 2]:
                    if len(datestring[i]) == 1:
                        datestring[i] = '0' + datestring[i]
                datestring = '-'.join(datestring)
                # datestring = m.group(1)
                # for i in [2, 3]:
                #     if len(m.group(i)) == 1:
                #         datestring += '-0' + m.group(i)
                #     else:
                #         datestring += '-' + m.group(i)
                print("出版日期为：%s" % datestring)
                self.publish_date = datestring
                return True
            else:
                self.publish_date = "0000-00-00"
                return True
        m = re.search(r"(\d+)年(\d+)月(\d+)日", r.findall(c)[-1])
        datestring = m.group(1)
        for i in [2, 3]:
            if len(m.group(i)) == 1:
                datestring += '-0' + m.group(i)
            else:
                datestring += '-' + m.group(i)
        # print("出版日期为：%s" % datestring)
        self.publish_date = datestring

    def have_saved(self):
        filename = hashlib.md5()
        filename.update(self.title.encode("utf8"))
        return os.path.exists("Data/" + filename.hexdigest())
        # if os.path.exists("Data/" + filename.hexdigest()):
        #     with open("Data/" + filename.hexdigest(), 'r', encoding="utf8") as f_saved:
        #         n1 = hashlib.md5()
        #         n1.update(f_saved.read().encode("utf8"))
        #     n2 = hashlib.md5()
        #     n2.update(json.dumps(self.__dict__, ensure_ascii=False, sort_keys=True, indent=4).encode("utf8"))
        #     if n1 == n2:
        #         return True
        #     else:
        #         return False
        # else:
        #     return False

    def save_sql(self, dbname): # 只能在save完毕后使用！
        if "征集公告" in self.title or "公示" in self.title or "公开征集" in self.title \
                or "评审结果公告" in self.title or "笔试" in self.title or "面试" in self.title or '公开招' in self.title \
                or "录用公务员" in self.title or "征集" in self.title or '培训班' in self.title:
            return False

        fieldnamelist = ['id', 'catid', 'typeid', 'title', 'style', 'thumb', 'keywords', 'description', 'posids',
                         'url', 'listorder', 'status', 'sysadd', 'islink', 'username', 'inputtime', 'updatetime',
                         'content', 'publish_date', 'public_no',
                         'meta_policy', 'base_policy', 'supply_policy', 'main_policy', 'guest_policy', 'support_policy', 'expires_date',
                         'tags', 'passtime', 'departments', 'depts', 'memo', 'isfront', 'adminmemo', 'law_policy', "hashid", "orig_url"]
        filename = hashlib.md5()
        filename.update(self.title.encode("utf8"))

        if not self.have_saved():
            self.save()
        with open("Data/" + filename.hexdigest(), 'r', encoding="utf8") as f:
            d = json.loads(f.read())
        if not d['ispolicy']:
            return True
        # INSERT INTO `t_policy`(catid,typeid,title,style,thumb,keywords,description,posids,url,listorder,status,sysadd,islink,username,inputtime,updatetime,content,publish_date,public_no,meta_policy,base_policy,supply_policy,main_policy,guest_policy,support_policy,expires_date,tags,passtime,departments,depts,memo,isfront,adminmemo,law_policy) VALUES (0, '0', '关于开展知识产权分析服务情况专项调查的通知', '', '', '', '', '0', '', '0', '0', '0', '0', 'consulting', '1479222385', '1479222385', '内容', '2012-07-10', '', ',,', ',,', ',,', ',,', ',,', ',,', '0000-00-00', '', null, '0', '', '', '0', '', ',,');
        fieldname = ', '.join(fieldnamelist[1:])
        # fieldcontent = "'" + "', '".join(str(d[key]) for key in fieldnamelist[1:]).replace("\n", "\\n") + "'"
        fieldcontent = "'" + "', '".join(str(d[key]) for key in fieldnamelist[1:]) + "'"
        fieldcontent = fieldcontent.replace("'null'", "null")

        s = "INSERT INTO `" + dbname + "`(" + fieldname + ") VALUES (" + fieldcontent + ");"

        s = ''.join(s.splitlines())

        while len(s.splitlines()) > 1:
            s = ''.join(s.splitlines())

        # s = "INSERT INTO `" + dbname + "` VALUES ('" + "', '".join(str(d[key]) for key in fieldnamelist).replace("\n", "\\n") + "');"
        with open("SQL/" + filename.hexdigest(), 'w', encoding="utf8") as f:
            f.write(s)

    def get_attachment(self, path, online_path):
        if "征集公告" in self.title or "公示" in self.title or "公开征集" in self.title \
                or "评审结果公告" in self.title or "笔试" in self.title or "面试" in self.title or '公开招' in self.title \
                or "录用公务员" in self.title or "征集" in self.title or '培训班' in self.title:
            return False

        b = BeautifulSoup(self.content, "html.parser")
        for att in b.find_all("a", href=True):
            if len(att["href"].split("/")) <= 1:
                continue
            if len(att["href"].split("/")[-1].split(".")) <= 1:
                continue
            if att["href"].split("/")[-1].split(".")[-1][:3].lower() in ['jsp', 'com', 'htm', 'dco', 'jpg'] or att["href"].split("/")[-1].split(".")[-1][:2].lower() in ['cn']:
                continue
            # if att["href"].split("/")[-1].split(".")[-1][:3] == 'com':
            #     continue
            filename = hashlib.md5()
            filename.update(att["href"].encode("utf8"))
            try:
                # r = requests.get(att["href"], timeout=10)
                r = requests.get(parse.urljoin(self.orig_url, att["href"]), timeout=10)
                with open(path + filename.hexdigest() + '.' + att["href"].split("/")[-1].split(".")[-1], 'wb') as f:
                    f.write(r.content)
                # att["href"] = "/Attachments/Guangdong/20161130/" + filename.hexdigest() + '.' + att["href"].split("/")[-1].split(".")[-1]
                att["href"] = online_path + filename.hexdigest() + '.' + \
                              att["href"].split("/")[-1].split(".")[-1]
                self.content = str(b)
            except:
                att["href"] = parse.urljoin(self.orig_url, att["href"])
                self.content = str(b)
                print(self.orig_url, att)

def load_jsonlist(file):
    with open(file, 'r', encoding="utf8") as f:
        return json.loads(f.read())

# btime = time.time()
# with open("Beijing-json.txt", 'r', encoding="utf8") as f:
#     diclist = json.loads(f.read())
#
# count = 0
#
# for dic in diclist:
#     # print([k for k in dic])
#     a = Policy(dic)
#     a.get_attachment("Attachments/")
#     a.save_sql('t_policy')
#     # c = BeautifulSoup(a.content, "html.parser")
#     # for i in c.find_all("a", href=True):
#     #     if "mailto" in i["href"]:
#     #         continue
#     #     r = requests.get(i["href"])
#     #     if r.headers['content-type'] != 'text/html':
#     #         print('\t'.join([i['href'], i.get_text()]))
#
#
#     # print(a.title)
#     # a.tag()
#     # a.save_sql('t_policy')
#     # count += 1
#     # print("%s / %s have done: %s%%" % (count, len(diclist), str(count/len(diclist)*100.0)[:5]))
#     # print("time: %.3f" % float(time.time() - btime))
#     # print(format("该条记录结束", "■^50s"))
