select top 10 * from plu order by saleprice
select outtradeno, * from orderselfapp where CONVERT(char(4), createtime, 120) = '2020'
select * from ordercomselfapp where orderid like '0020%'

--delete from orderselfapp where CONVERT(char(4), createtime, 120) = '2020'
--delete from ordercomselfapp where orderid like '0020%'

--delete from orderselfapp where orderid = '002000000003'
--delete from ordercomselfapp where orderid = '002000000003'

select * from orderselfapp where convert(char(10),createtime, 120) >= '2020-11-18' order by createtime desc
select * from ordercomselfapp where orderid in ('002000000501', '002000000500')

select * from plu where comname like '%¹ºÎï´üÐ¡%'
select * from pluOnline

select	stock.comid,
		stock.quantity
from	stock,
		plu
where	stock.comid = plu.comid
and		plu.status in ('A','B','C','') 

select * from pluOnline

select	stock.comid,
		stock.quantity
from	stock,
		pluOnline,
		plu
where	stock.comid=pluOnline.comid
and		pluOnline.comid=plu.comid
and		pluOnline.status=1
and		plu.status in ('A','B','C','')
