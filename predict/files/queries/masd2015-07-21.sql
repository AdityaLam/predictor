
USE [SAPDATA]
GO

SELECT   MAX(ITEM.[MATERIAL]) AS MATERIAL
                ,[MRP_ELEMENT] AS PO_NUMBER
                ,MAX(SCHED.[ERF_NUMBER]) AS ERF_NUMBER
                ,MAX(SCHED.[ERF_ITEM]) AS ERF_ITEM
                ,MAX([ERF_TYPE]) AS ERF_TYPE
                ,CASE
                        WHEN CONVERT(int, MAX([SUBMIT_DATE])) = 0
                                THEN NULL
                        ELSE
                                CONVERT(Datetime, stuff(stuff(stuff(MAX([SUBMIT_DATE]) + MAX([SUBMIT_TIME]), 9, 0, ' '), 12, 0, ':'), 15, 0, ':'))
                 END AS SUBMIT_DATE
                ,CASE
                        WHEN CONVERT(int, MAX([APPROVED_DATE])) = 0
                                THEN NULL
                        ELSE
                                CONVERT(Datetime, stuff(stuff(stuff(MAX([APPROVED_DATE]) + MAX([APPROVED_TIME]), 9, 0, ' '), 12, 0, ':'), 15, 0, ':'))
                 END AS APPROVED_DATE
                ,CASE
                        WHEN CONVERT(int, MAX(QUOTE_IT.[SEND_DATE])) = 0
                                THEN NULL
                        ELSE
                                CONVERT(Datetime, stuff(stuff(stuff(MAX(QUOTE_IT.[SEND_DATE]) + MAX(QUOTE_IT.[SEND_TIME]), 9, 0, ' '), 12, 0, ':'), 15, 0, ':'))
                 END AS QUOTE_SEND_DATE
                ,CASE
                        WHEN CONVERT(int, MAX(QUOTE_IT.[RETURN_DATE])) = 0
                                THEN NULL
                        ELSE
                                CONVERT(Datetime, stuff(stuff(stuff(MAX(QUOTE_IT.[RETURN_DATE]) + MAX(QUOTE_IT.[RETURN_TIME]), 9, 0, ' '), 12, 0, ':'), 15, 0, ':'))
                 END AS QUOTE_RETURN_DATE
                ,CASE
                        WHEN CONVERT(int, MIN([AEDAT])) = 0
                                THEN NULL
                        ELSE
                                CONVERT(Datetime, MIN([AEDAT]))
                 END AS PO_PLACE_DATE
                ,MAX([RCTENDAT2]) AS RECEIPT_DATE
                ,MAX(ITEM.[COST_MAX]) AS COST
                ,MAX([RCTQPRI]) AS FINAL_COST
                ,MAX([ITEM_QTY]) AS QUANTITY
        FROM [SAPDATA].[dbo].[ZMERF_SCHED] AS SCHED
        LEFT JOIN [SAPDATA].[dbo].[ZMERF_ITEM] AS ITEM ON  CONVERT(int, ITEM.ERF_NUMBER) = CONVERT(int, SCHED.ERF_NUMBER) AND CONVERT(int, ITEM.ERF_ITEM) = CONVERT(int, SCHED.ERF_ITEM)
        LEFT JOIN [SAPDATA].[dbo].[ZMERF_HEAD] AS HEAD ON CONVERT(int, SCHED.ERF_NUMBER) = CONVERT(int, HEAD.ERF_NUMBER)
        LEFT JOIN [Sharedat].[dbo].[RCTREC] AS RCTREC ON SCHED.MRP_ELEMENT = RCTPO AND 10*CONVERT(int, RCTREC.RCTPOLIN) = CONVERT(int, SCHED.MRP_ITEM)
        LEFT JOIN [SAPDATA].[dbo].[ZMERF_QUOTE] AS QUOTE ON CONVERT(int, SCHED.ERF_NUMBER) = CONVERT(int, QUOTE.ERF_NUMBER) AND CONVERT(int, QUOTE.ERF_ITEM) = CONVERT(int, SCHED.ERF_ITEM)
                AND SUBSTRING(QUOTE.[VENDOR_NO], PATINDEX('%[^0]%', QUOTE.[VENDOR_NO]+'.'), LEN(QUOTE.[VENDOR_NO])) = SUBSTRING(RCTREC.[VENCODE], PATINDEX('%[^0]%', RCTREC.[VENCODE]+'.'), LEN(RCTREC.[VENCODE]))
        LEFT JOIN [SAPDATA].[dbo].[ZMERF_QUOTE_IT] AS QUOTE_IT ON CONVERT(int, QUOTE_IT.ERF_QUOTE) = CONVERT(int, QUOTE.ERF_QUOTE)
        LEFT JOIN [SAPDATA].[dbo].[EKPO] AS HISTORY ON SCHED.MRP_ELEMENT = EBELN AND CONVERT(int, EBELP) = CONVERT(int, SCHED.MRP_ITEM)
        WHERE MRP_ELEMENT LIKE '4700%%%%%%' AND RCTENDAT2 IS NOT NULL AND (
ITEM.MATERIAL LIKE '714-064081-5%%'
OR ITEM.MATERIAL LIKE '714-064381-5%%'
OR ITEM.MATERIAL LIKE '839-169479-0%%'
OR ITEM.MATERIAL LIKE '839-222229-0%%'
        )
        GROUP BY [MRP_ELEMENT]
        ORDER BY MATERIAL DESC

GO                
    