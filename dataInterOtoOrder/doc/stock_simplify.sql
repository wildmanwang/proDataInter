  SELECT dbo.stock.comid,   
         dbo.plu.barcode,   
         dbo.plu.comname,   
         dbo.plu.comtype, 
			dbo.plu.unit ,
			dbo.plu.standards,
			dbo.plu.package,
         sum(dbo.stock.quantity) as sumquantity,   
         sum(dbo.stock.quantity * dbo.stock.price) / sum(dbo.stock.quantity) as avgprice,
		 	sum(dbo.stock.quantity * dbo.stock.price)  as jine,
		 	dbo.plu.saleprice,
		 	dbo.plu.promotionsaleprice,
		 	dbo.plu.vipprice,		 
		 	sum(dbo.stock.quantity * dbo.stock.saleprice)  as salepricejine,
		 	o.orderedqty as orderedqty,	/*sum去掉*/
		 	'' as eflag,
		 	sum(isnull(salecom.quantity,0.00)) as saleqty,
		 	dbo.plu.vendorid,
			dbo.plu.vendorname,
			dbo.plu.daysales,
			dbo.plu.weeksales,
			dbo.plu.monthsales,
			dbo.plu.stddms,
			dbo.plu.lastaddstodate,
			dbo.plu.lastaddstoquan,
			dbo.plu.lastorderdate,
			dbo.plu.lastorderquan,
			case when (dbo.plu.status not in( '', 'A', 'B', 'C' ) Or dbo.plu.lowsalesum < 0.0) then '1' else '0' end  stopYN
			,case when (sum(stock.quantity)<>0 and plu.monthsales<>0) then sum(stock.quantity)/plu.monthsales*day(dateadd(mm,1,getdate())-day(getdate())) else 0 end  zdays /*周转天数*/
			,plu.lastsaletime	/*最后销售日期*/
			,datediff(day,plu.lastsaletime,getdate()) nosaledays /*滞销天数*/
    FROM dbo.plu,
         dbo.stock 
			Left join ( select a.comid,sum(a.quantity+a.giftquantity-a.arrive-a.giftarrive) as orderedqty
							from orderdetail a, ordermain b
							where a.orderid = b.orderid and b.status='有效' and (b.flag='正式单据' or b.flag='已制凭证')
							Group By a.comid
						 ) o on (dbo.stock.comid = o.comid)
			Left join v_salecom_sum salecom On (('0'='0' and 1=2) or ('0'='1' and ( stock.comid = salecom.comid )) )
   WHERE ( dbo.plu.comid = dbo.stock.comid ) 
	 and (stock.warehouseid <> '') and (stock.comid = '00021509') group by    
			dbo.stock.comid,   
         dbo.plu.barcode,   
         dbo.plu.comname,   
         dbo.plu.comtype,
			dbo.plu.unit ,
			dbo.plu.standards,
			dbo.plu.package,
		 	dbo.plu.saleprice,
			dbo.plu.promotionsaleprice,
		 	dbo.plu.vipprice,
			o.orderedqty,
			dbo.plu.vendorid,
			dbo.plu.vendorname,
		   dbo.plu.daysales,
		   dbo.plu.weeksales,
		   dbo.plu.monthsales,
		   dbo.plu.stddms,
			dbo.plu.lastaddstodate,
			dbo.plu.lastaddstoquan,
			dbo.plu.lastorderdate,
			dbo.plu.lastorderquan,
			dbo.plu.status,
			dbo.plu.lowsalesum
			,plu.lastsaletime
	having sum(dbo.stock.quantity) <> 0.0 and 9=9	/*and 9=9 用于替换*/
union all
	SELECT dbo.stock.comid,   
         dbo.plu.barcode,   
         dbo.plu.comname,   
         dbo.plu.comtype, 
			dbo.plu.unit , 
			dbo.plu.standards,
			dbo.plu.package, 
         sum(dbo.stock.quantity) as sumquantity,   
         avg(dbo.stock.price) as avgprice,
		   sum(dbo.stock.quantity * dbo.stock.price)  as jine,
		 	dbo.plu.saleprice,
		 	dbo.plu.promotionsaleprice,
		 	dbo.plu.vipprice,	
		 	sum(dbo.stock.quantity * dbo.stock.saleprice)  as salepricejine,
		 	o.orderedqty as orderedqty,	/*sum去掉*/
		 	'' as eflag,
		 	sum(isnull(salecom.quantity,0.00)) as saleqty,
			dbo.plu.vendorid ,
			dbo.plu.vendorname,
			dbo.plu.daysales,
			dbo.plu.weeksales,
			dbo.plu.monthsales,
			dbo.plu.stddms,
			dbo.plu.lastaddstodate,
			dbo.plu.lastaddstoquan,
			dbo.plu.lastorderdate,
			dbo.plu.lastorderquan,
			case when (plu.status not in( '', 'A', 'B', 'C' ) Or plu.lowsalesum < 0.0) then '1' else '0' end  stopYN
			,case when (sum(stock.quantity)<>0 and plu.monthsales<>0) then sum(stock.quantity)/plu.monthsales*day(dateadd(mm,1,getdate())-day(getdate())) else 0 end  zdays /*周转天数*/
			,plu.lastsaletime	/*最后销售日期*/
			,datediff(day,plu.lastsaletime,getdate()) nosaledays /*滞销天数*/
    FROM dbo.plu ,   
         dbo.stock
			Left join ( select a.comid,sum(a.quantity+a.giftquantity-a.arrive-a.giftarrive) as orderedqty
							from orderdetail a, ordermain b
							where a.orderid = b.orderid and b.status='有效' and (b.flag='正式单据' or b.flag='已制凭证')
							Group By a.comid
						 ) o on (dbo.stock.comid = o.comid)
		   Left join v_salecom_sum salecom On (('0'='0' and 1=2) or ('0'='1' and ( stock.comid = salecom.comid )) )
   WHERE ( dbo.plu.comid = dbo.stock.comid )  
	 and (stock.warehouseid <> '') and (stock.comid = '00021509') group by    
			dbo.stock.comid,   
         dbo.plu.barcode,   
         dbo.plu.comname,   
         dbo.plu.comtype,
			dbo.plu.unit ,
		   dbo.plu.standards,
			dbo.plu.package,
			dbo.plu.saleprice,
			dbo.plu.promotionsaleprice,
		 	dbo.plu.vipprice,
			o.orderedqty,
			dbo.plu.vendorid,
			dbo.plu.vendorname,
			dbo.plu.daysales,
			dbo.plu.weeksales,
			dbo.plu.monthsales,
			dbo.plu.stddms,
			dbo.plu.lastaddstodate,
			dbo.plu.lastaddstoquan,
			dbo.plu.lastorderdate,
			dbo.plu.lastorderquan,
			dbo.plu.status,
			dbo.plu.lowsalesum
			,plu.lastsaletime
	having sum(dbo.stock.quantity) = 0.0 and 9=9	/*and 9=9 用于替换*/
