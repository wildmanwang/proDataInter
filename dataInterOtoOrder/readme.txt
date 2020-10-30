【发到家项目总览】
业务负责人：刘俊
客户超市：发到家
客户技术：王总

【vpn连接】
类型：PPTP-需要加密-允许使用协议(2/3)
user:sl
password:SL_VPN_123456

【客户测试数据库MSSQL连接】
server:183.6.102.205
user:sa
password:ngt3000pos

【鸿商ERP】
user:1111
password:2
server:192.168.1.253（测试-pos）1111,111
server:192.168.1.254（真实-核销）1111,123

【线上小程序】
名称：九鸿广场

【数据结构】
商品：select * from currentdb..plu where lowsalesum >= 0.0 and plu.status in ('A','B','C','') 
订单：？

【接口需求】
1 数据上传：商品等基础数据上传（标准接口）
2 数据下载：订单数据下传（非标准接口，直接访问数据库）
3 订单核销：线上订单到线下提货（标准接口，但不确定是否能用？）
