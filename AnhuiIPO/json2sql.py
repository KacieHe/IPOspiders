import tpolicy, os, json, time

beginstr = '''SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_policy_ah`
-- ----------------------------
DROP TABLE IF EXISTS `t_policy_ah`;
CREATE TABLE `t_policy_hn` (
`id`  mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT ,
`catid`  smallint(5) UNSIGNED NOT NULL DEFAULT 0 ,
`typeid`  smallint(5) UNSIGNED NOT NULL DEFAULT 0 ,
`title`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`style`  char(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`thumb`  char(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`keywords`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`description`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`posids`  tinyint(1) UNSIGNED NOT NULL DEFAULT 0 ,
`url`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`listorder`  int(10) UNSIGNED NOT NULL DEFAULT 0 ,
`status`  tinyint(3) UNSIGNED NOT NULL DEFAULT 99 ,
`sysadd`  tinyint(1) UNSIGNED NOT NULL DEFAULT 0 ,
`islink`  tinyint(1) UNSIGNED NOT NULL DEFAULT 0 ,
`username`  varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`inputtime`  int(10) UNSIGNED NOT NULL DEFAULT 0 ,
`updatetime`  int(10) UNSIGNED NOT NULL DEFAULT 0 ,
`content`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`publish_date`  date NULL DEFAULT NULL ,
`public_no`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`meta_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`base_policy`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`supply_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`main_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`guest_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`support_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`expires_date`  date NULL DEFAULT NULL ,
`tags`  varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`passtime`  datetime NULL DEFAULT NULL ,
`departments`  int(10) UNSIGNED NULL DEFAULT 0 ,
`depts`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`memo`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`isfront`  int(10) UNSIGNED NOT NULL DEFAULT 0 ,
`adminmemo`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`law_policy`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`admincolumn`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' ,
`hashid`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 0 ,
`orig_url`  varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' ,
PRIMARY KEY (`id`),
INDEX `status` (`status`, `listorder`, `id`) USING BTREE ,
INDEX `listorder` (`catid`, `status`, `listorder`, `id`) USING BTREE ,
INDEX `catid` (`catid`, `status`, `id`) USING BTREE ,
INDEX `publish_date` (`listorder`, `publish_date`, `updatetime`) USING BTREE ,
INDEX `hashid` (`hashid`) USING BTREE
)
ENGINE=MyISAM
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Auto increment value for `t_policy_ah`
-- ----------------------------
'''

n = 0
btime = time.time()
for file in os.listdir("Json"):
    with open("Json/" + file, 'r', encoding="utf8") as f:
        d = f.read()
    a = tpolicy.Policy(json.loads(d))
    a.get_attachment("Atta/", "/Attachments/Anhui/20161214/")
    a.save_sql("t_policy_ah")

    n += 1
    print(n, '-', round(time.time()-btime, 3))

d = []
for f in os.listdir("SQL"):
    with open("SQL/" + f, 'r', encoding="utf8") as fi:
        d.append(fi.read() + '\n')

with open ("Anhui-sql.sql", 'w', encoding="utf8") as f:
    f.write(beginstr)
    f.writelines(d)