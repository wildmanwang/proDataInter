前言：
1 该程序将以后台服务的形式运行，请按步骤安装好，并设置【自动启动】
2 该程序在启动后，将会删除APP点菜数据库中的菜品及类别资料，请对【双方数据都做好备份】
3 科脉软件需要按微信点餐来部署，包括：开启微信订单服务、开启微信点餐助手等

步骤：
1：删除APP端接口表相关的外键（如果没有外键请跳过）
2：对APP端数据库登录用户开放增删改查以及创建表的权限（授予管理员权限请跳过）
    2.1 至少对以下表开放增删改查：
        2.1.1 Dine_ClassSub
        2.1.2 Dine_Goods
        2.1.3 Dine_GOODSBOM
        2.1.4 Dine_cooknote
        2.1.5 Dine_GoodsCookNote
        2.1.6 Dine_sales
        2.1.7 Dine_salesdd
    2.2 如果不开放创建表的权限，请预先执行以下建表脚本（授予建表权限请跳过）：
        create table interTmp (
          Dine_ID         varchar(50) not null,
          busiDate        varchar(10) not null,
          app_billno      varchar(50) not null,
          primary key ( Dine_ID, busiDate, app_billno ) )
        go
        create table interTmp0 (
          Dine_ID         varchar(50) not null,
          busiDate        varchar(10) not null,
          app_billno      varchar(50) not null,
          primary key ( Dine_ID, busiDate, app_billno ) )
        go

3：设置【config】中的各项参数
    [Database_app]                      APP点餐数据库连接参数设置
    host = 119.23.61.176                服务器地址：例子是命名实例的设置格式，默认实例只需要写服务器名
    user = dine_test                    登录用户名
    password = 111111                   登录密码
    database = Dine_app                 数据库

    [Database_erp]                      ERP数据库连接参数设置，以下各项同上
    host = PC-20170506RFIY\MSSQL2008
    user = sa
    password = 111111
    database = db_name

    [Other]
    bill_get_interval = 10              单据传输间隔，默认10秒，可根据实际情况调整
    Dine_ID = cb9d3903-eb2d-40e4-aaae-39bc18b9a393  APP端门店编码
    branch_no = 00                      ERP软件的门店编码
    tabnumber = 001                     APP点餐对应的台位号
4：把服务程序【inerService.exe】列入防火墙、杀毒软件白名，因为作为作为服务程序可能会被拦截
5：操作服务程序时，请右键点击命令提示符，选择“以管理员身份运行”，服务操作命令如下：
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
