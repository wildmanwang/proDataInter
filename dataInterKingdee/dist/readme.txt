前言：
1 该程序将以后台服务的形式运行，请按步骤安装好，并设置【自动启动】
2 请备份【金蝶数据库】

步骤：
1：在科脉数据库所在服务器上，建立一个空库，用于控制数据对接
2：在金蝶后台库中配置基础资料自动分配方案
3：设置【config】中的各项参数
[frontEnd]				科脉端（直连数据库）
host = .				连接地址，IP或者IP:port
user = sa				用户名
password =  			密码
database = kmcy_v8	    数据库名

[backEnd]				金蝶端（http连接）
host = https://***.ik3cloud.com	服务器地址
user = administrator	用户名
password =          	密码
database = 				后端数据库名（如果是http连接，忽略此参数）

[controlEnd]			控制端（新建的空库，直连数据库）
host = .				连接地址，IP或IP:port
user = sa				用户名
password =  			密码
database =  			数据库名

[control]
timingBaseInterval = 100	基础资料同步时间间隔，单位秒
timingBusiDay = 0			单据同步日期 0：同步当天数据 1：同步前一天数据
timingBusiTime = 20:20		单据同步时间，5位数字，例如：03:30

[org]					机构配置：左边是科脉机构编号；右边是对应的金蝶机构ID
000 = 1
000010 = 104787
000011 = 104788

[payment]				支付方式配置：左边是科脉支付编号；右边是对应的金蝶支付ID
01 = JSFS01_SYS
other = JSFS02_SYS

[busiBackKingdee]			默认参数
defaultOrgNo = 100          默认机构
clsBigNo = 01               默认食品大类
deptNo = BM000001			默认部门编号
userNo = 00001				默认用户编号

4：把服务程序【inerService.exe】列入防火墙、杀毒软件白名单，因为作为服务程序可能会被误拦截
5：操作服务程序时，右键点击命令提示符，选择“以管理员身份运行”，服务操作命令如下：
    #1.安装服务
    interService.exe install
    #2.让服务自动启动
    interService.exe --startup auto install
    #3.启动服务
    interService.exe start
    #4.重启服务
    interService.exe restart
    #5.停止服务
    interService.exe stop
    #6.删除/卸载服务
    interService.exe remove
6：查看服务程序目录下的日志文件【service.log】信息，如有ERROR信息无法解决，请联系软件供应商
