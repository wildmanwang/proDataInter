新需求：
黄经理（建店）乐购东莞卡：当现金支付，另外记录券号


数据结构:
	d_t_bill_pay0.cOuterCode		第三方会员卡号/票券号
	d_t_bill_pay0.bankcard_no		第三方会员交易流水号，冲正和被冲正的记录都为空

空接口测试程序
	科脉标准程序修改
手输折扣卡接口
	积分
	测试环境
二维码电子卡接口
	储值消费/消费冲正
	测试环境
	扫码枪
条码银商卡接口
	测试环境
	读卡器
	储值消费/消费冲正
海鲜加工券
	现金券核销
消费积分接口
	积分/积分扣减
代码优化
	代码模块化
	增加避免连续点击误操作判断

科脉支付类型（ePayType）
	折扣卡
	电子会员
	银商卡
	票券

嘉荣准备项：
搭建收银软硬件环境
	昂捷会员环境：
		10.10.90.10：8095转113.105.132.43：8095已开通
		接口调用地址:http://113.105.132.43:8095/enjoy/Service userno:B46878AF-BDC6-4B4A-B7B7-5BCD1A1348F0 key:10850078
		测试会员
			顾客编码：55000022026
			会员卡号：501344724
			电话号码：13899999999
		接口错误
			查询会员信息：805：未将对象引用设置到对象的实例。
			增减积分冲正：007：您没有调用[积分增减冲正]
			优惠券初始化：-9：起始卡号不能为空 ——根本没这个字段
			优惠券批量查询：应用程序中的服务器错误 ——HTML格式，无法找到资源
			优惠券核销冲正：007：您没有调用[优惠券核销冲正]
会员卡刷卡测试环境，包括银商卡刷卡器、二维码扫码枪、3种会员数据
会员刷卡后分别需要查询哪些字段？

小程序测试环境：
119.23.235.56
user:Administrator
pwd:Alan-liukun1121!
dbpwd:Windows2008

嘉荣3楼：spar-wifi
JRspar123

DES加密解密的PB实现
https://blog.csdn.net/JasonFriday/article/details/94494886

MD5加密的PB实现
https://blog.csdn.net/xiajinxian/article/details/46627527

HTTP请求的PB实现
https://bbs.csdn.net/topics/390552901
https://blog.csdn.net/smilysoft/article/details/51498174
https://www.cnblogs.com/Bokeyan/p/12653117.html
https://blog.csdn.net/softvery/article/details/87556945
https://blog.csdn.net/pcwe2002/article/details/103047572

JSON解析
https://blog.csdn.net/smilysoft/article/details/51497244

docfor/d_w_inputdoc_kb_vipmember
docfor/d_w_inputdoc_kb_vipmember_ifadv
docfor/d_w_fore_opentable_cvip_arrearage
docfor/d_w_vipmember_finditem
docfor/d_w_vipmember_morecard


需求/问题跟进：
20200724：全部会员操作，不需要查询，直接支付
	解决：当天已更新
20200724：银商卡支付报错：无效金额
	解决：当天已更新
20200724：Error calling external object function send at line 18 in function of_post of object nvo_httprequest
	原因：网络问题
	解决：可优化体验，捕捉错误
