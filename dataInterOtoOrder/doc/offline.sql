select top 10 * from plu order by saleprice
select outtradeno, * from orderselfapp where CONVERT(char(4), createtime, 120) = '2020'
select * from ordercomselfapp where orderid like '0020%'

--delete from orderselfapp where CONVERT(char(4), createtime, 120) = '2020'
--delete from ordercomselfapp where orderid like '0020%'

--delete from orderselfapp where orderid = '002000000003'
--delete from ordercomselfapp where orderid = '002000000003'

select * from orderselfapp where orderid in ('002000000501', '002000000500')
select * from ordercomselfapp where orderid in ('002000000501', '002000000500')
