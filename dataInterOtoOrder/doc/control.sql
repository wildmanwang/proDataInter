select * from busiParas
select * from InterCompleted

update busiParas set sValue = '2020-11-18 00:00:00' where sCode = 'order_downline'

insert into InterCompleted ( busiType, dataType, sNumber, iNumber, sRelated, sName, sBranch, sDate ) 
values ( 'order', 'S', '6LCNR000400B', null, '002000000003', '', '100', '2020-11-19 17:35:42' ) 

select    dataType,           sNumber,           iNumber,           sRelated,           sName,           sBranch,           sTime 
from      InterCompleted where     busiType = 'item' and       sBranch = '01' and       sTime >= '' and       sTime <= '' 
