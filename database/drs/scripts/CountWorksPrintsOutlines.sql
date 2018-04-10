set  @AllWorksCount = ( select count(*) from drs.Works);

select@WorksPrintOROutline = (select count(*) from drs.Works w left outer join drs.Outlines o using (workId) ) ; -- left outer join drs.PrintMasters p using (workId) where p.PrintMasterId is  null); --  or  o.outLineId is not null);

set @WorksNoOutlineNoPrint = (select count(*) from drs.Works w left outer join drs.Outlines o using (workId) left outer join drs.PrintMasters p using (workId) where p.PrintMasterId is  null and o.outLineId is null);

set @WorksNoOutline =  (select count(*) from drs.Works w left outer join drs.Outlines o using (workId) where o.outlineId is null);

set @WorksWithOutlineIJ=  (select count(*) from drs.Works w inner join drs.Outlines o using (workId));

set @WorksNoPrintLO =  (select count(*) from drs.Works w left outer join drs.PrintMasters p using (workId) where p.PrintMasterId is null);


set @WorksPrintIJ=  (select count(*) from drs.Works w inner join drs.PrintMasters p using (workId) );

set @WorksBothPrintOutlineIJ   =(select count(*) from drs.Works w inner join drs.Outlines o using (workId) inner join drs.PrintMasters p using (workId) );


select @AllWorksCount,@WorksPrintOROutline , @WorksNoOutlineNoPrint, @WorksNoOutline,@WorksWithOutlineIJ,@WorksNoPrintLO,@WorksPrintIJ,@WorksBothPrintOutlineIJ;