SELECT t.INN, t.KPP, MAX(t.ORG_NAME) as ORG_NAME
         ,t.ОтчетГод
         ,t.Период
    ,SUM(t.GR9) as GR9

    ,SUM(t.GR10) GR10

FROM (

 SELECT isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ) as INN
        ,tab4.КПП as KPP
           ,tab3.ОтчетГод
         ,tab3.Период
        ,MAX(ISNULL(tab4.НаимОрг, tab4.Фамилия + ' ' + tab4.Имя + ' ' + ISNULL(tab4.Отчество, '') )) as ORG_NAME

        ,SUM(case when tab2.КодПт in ('232', '251', '252', '253', '254', '274', '275', '276', '277', '287', '288', '297', '310', '320', '330') then tab.НалБаза else 0 end) as GR9
        ,SUM(case when tab2.КодПт in ('231', '224', '225', '226', '227', '290') then tab.НалБаза else 0 end) as GR10
  FROM  [FNS_DECLARATION].dbo.ND01_РасчАкц tab2
      join   [dbo].[ND01_РасчОперПТКод] tab on tab2.Ид=tab.ИдРасчАкц
    inner join [FNS_DECLARATION].dbo.ND01_Документ tab3
        on tab3.Ид = tab2.ИдДокумент
    inner join [FNS_DECLARATION].dbo.ND01_СвНП tab4
        on tab4.ИдДокумент = tab3.Ид
  WHERE tab3.Актуальность = 1 
   and  tab.КодПок='10001'
  GROUP BY isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ), tab4.КПП
     ,tab3.ОтчетГод
         ,tab3.Период

UNION ALL  
 SELECT isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ) as INN
        ,tab4.КПП as KPP
           ,tab3.ОтчетГод
         ,tab3.Период
        ,MAX(ISNULL(tab4.НаимОрг, tab4.Фамилия + ' ' + tab4.Имя + ' ' + ISNULL(tab4.Отчество, '') )) as ORG_NAME

        ,SUM(case when tab2.КодПт in ('232', '251', '252', '253', '254', '274', '275', '276', '277', '287', '288', '297', '310', '320', '330') then tab.НалБаза else 0 end) as GR9
        ,SUM(case when tab2.КодПт in ('231', '224', '225', '226', '227', '290') then tab.НалБаза else 0 end) as GR10
  FROM  [FNS_DECLARATION].dbo.ND02_РасчАкц tab2
      join   [dbo].[ND02_РасчОперПТРФКод] tab on tab2.Ид=tab.ИдРасчАкц
    inner join [FNS_DECLARATION].dbo.ND02_Документ tab3
        on tab3.Ид = tab2.ИдДокумент
    inner join [FNS_DECLARATION].dbo.ND02_СвНП tab4
        on tab4.ИдДокумент = tab3.Ид
  WHERE tab3.Актуальность = 1 
   and  tab.КодПок='10001'
  GROUP BY isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ), tab4.КПП
     ,tab3.ОтчетГод
         ,tab3.Период

UNION ALL  
 SELECT isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ) as INN
        ,tab4.КПП as KPP
           ,tab3.ОтчетГод
         ,tab3.Период
        ,MAX(ISNULL(tab4.НаимОрг, tab4.Фамилия + ' ' + tab4.Имя + ' ' + ISNULL(tab4.Отчество, '') )) as ORG_NAME

        ,SUM(case when tab2.КодПт in ('232', '251', '252', '253', '254', '274', '275', '276', '277', '287', '288', '297', '310', '320', '330') then tab.НалБаза else 0 end) as GR9
        ,SUM(case when tab2.КодПт in ('231', '224', '225', '226', '227', '290') then tab.НалБаза else 0 end) as GR10
  FROM  [FNS_DECLARATION].dbo.ND03_РасчАкц tab2
      join   [dbo].[ND03_РасчОперПТРФКод] tab on tab2.Ид=tab.ИдРасчАкц
    inner join [FNS_DECLARATION].dbo.ND03_Документ tab3
        on tab3.Ид = tab2.ИдДокумент
    inner join [FNS_DECLARATION].dbo.ND03_СвНП tab4
        on tab4.ИдДокумент = tab3.Ид
  WHERE tab3.Актуальность = 1 
   and  tab.КодПок='10001'
  GROUP BY isnull(cast(tab4.ИННЮЛ as varchar(12)), tab4.ИННФЛ), tab4.КПП
     ,tab3.ОтчетГод
         ,tab3.Период
) t
--where t.ОтчетГод=2022 
--and t.Период=9
--and t.INN='0542001269'
GROUP BY t.INN, t.KPP   ,t.ОтчетГод
         ,t.Период
ORDER BY 4,5,1,2 desc
