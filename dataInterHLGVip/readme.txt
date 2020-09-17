【客户】
深圳欢乐谷
向日葵：596705801，1234（间接远程）
客户服务器：172.25.9.210，Happy2018
阿里云测试服务器：139.159.149.52，Alan-liukun1121!

【需求】
线上会员同步到科脉餐饮软件，要求实现会员折扣。
具体实现：
    会员注册：推送会员信息
    会员出示二维码：推送二维码动态码
    查询会员消费记录

【实施】
update vip set IdentityCardId = FlowId, FlowId = null where LEN(FlowId) > 0 and IdentityCardId is null;
