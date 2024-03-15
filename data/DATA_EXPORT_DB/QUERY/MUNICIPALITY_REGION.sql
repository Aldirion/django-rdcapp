SELECT public."Municipality"."Title", public."Municipality"."RegionID", public."Region"."Title" FROM public."Municipality"

LEFT JOIN public."Region" ON public."Municipality"."RegionID" = public."Region"."RegionID"

WHERE public."Municipality"."RegionID" = '32'

ORDER BY "ID" ASC 