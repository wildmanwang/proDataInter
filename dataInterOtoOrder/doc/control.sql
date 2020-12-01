select * from busiParas
select * from InterCompleted

update busiParas set sValue = '2020-11-30 01:00:00' where sCode = 'order_downline'

select    dataType,           sNumber,           iNumber,           sRelated,           sName,           sBranch,           sTime 
from      InterCompleted where     busiType = 'item' and       sBranch = '01' and       sTime >= '' and       sTime <= '' 

select sRelated from InterCompleted where busiType = 'order' and iStatus = 0 and sRelated in ('002000000003', '002000000652')

select * from plu
select * from pluOnline

update InterCompleted set iStatus = 0 where cID=10