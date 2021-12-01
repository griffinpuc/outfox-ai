/*
    CREDIT TO:
    https://stackoverflow.com/questions/12674600/creating-a-correlation-matrix-in-sql-server
*/

DECLARE query NVARCHAR(MAX);
DECLARE colsPivot NVARCHAR(MAX);

select @colsPivot = STUFF((SELECT distinct  ',' 
                      + quotename(tagA)
                    from yourtable t
            FOR XML PATH(''), TYPE
            ).value('.', 'NVARCHAR(MAX)') 
        ,1,1,'')

set @query 
  = 'select tagA, '+@colspivot+ '
     from 
     (
       select tagA tagA, tagB tagB, correlation
       from yourtable
       union all
       select tagB, tagA, correlation
       from yourtable
       union all
       select distinct tagA, tagA, 1.0
       from yourtable
      ) x
      pivot
      (
        max(correlation) 
        for tagB in ('+ @colspivot +')
      ) p'

exec(@query)


		
select @colsPivot = overlay((SELECT distinct  ',' 
                      + quotename(tagA)
                    from yourtable t
            FOR XML string_agg(''), TYPE
            ).value('.', 'NVARCHAR(MAX)') 
        placing '',from 1 for 1)


DECLARE mnquery := 'select tagA, '+@colspivot+ '
     from 
     (
       select tagA tagA, tagB tagB, correlation
       from yourtable
       union all
       select tagB, tagA, correlation
       from yourtable
       union all
       select distinct tagA, tagA, 1.0
       from yourtable
      ) x
      pivot
      (
        max(correlation) 
        for tagB in ('+ @colspivot +')
      ) p'

exec(@query)