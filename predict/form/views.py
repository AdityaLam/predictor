from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm, PartFormSet
from django.core.mail import EmailMultiAlternatives
from django.core import mail
import os
from yesterday.models import Part

script_dir = os.path.dirname(__file__)
rel_data = "../files/queries"
query_path = os.path.join(script_dir, rel_data)


def form(request):
    code_id = request.get_full_path().split('/')[-1]
    part = Part.objects.filter(id=code_id).first()
    name = part.name
    uid = part.uid
    email = part.email
    number = part.part
    name_form = NameForm({'uid':uid, 'name':name, 'email':email})
    formset = PartFormSet(initial=[{'number':number}])
    return render(request, 'form/parts.html', {'form': name_form, 'formset':formset})


def parts(request):
    if request.method == 'POST':
        name_form = NameForm(request.POST)
        part_form = PartFormSet(request.POST)
        if name_form.is_valid() and part_form.is_valid():
            uid = name_form.cleaned_data['uid']
            name = name_form.cleaned_data['name']
            email = name_form.cleaned_data['email']
            number = part_form.cleaned_data[0]['number']
            id_num = Part.objects.filter(uid=uid, part=number).first().id
            construct_query(part_form, id_num)
            email_query(name, email, id_num)
            return HttpResponse('query sent')
    else:
        return HttpResponse('something weird happened')

def construct_query(part_form, id_num):
    import re
    from datetime import datetime
    pattern = re.compile(r"^[0-9]{3}-[0-9]{6}-[0-9]{3}$")

    beginning = """
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
"""
    numbers = []

    for data in part_form.cleaned_data:
        if 'number' in data and pattern.match(data['number']):
            numbers.append("ITEM.MATERIAL LIKE '" + data['number'][:-3]+"%%%'")

    middle = "\nOR ".join(numbers)

    end = """
        )
        GROUP BY [MRP_ELEMENT]
        UNION ALL
        SELECT '%d', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL

GO                
    """ % int(id_num)
    with open(os.path.join(query_path, id_num + "-" + str(datetime.now().date()) + '.sql'), 'wb+') as query:
        query.write(bytes(beginning, 'UTF-8'))
        query.write(bytes(middle, 'UTF-8'))
        query.write(bytes(end, 'UTF-8'))

def email_query(name, email, id_num):
    from datetime import datetime
    from _thread import start_new_thread
    part = Part.objects.filter(id=id_num).first()
    subject, from_email, to_email = 'Query for ' + name, 'lampredictor@gmail.com', 'stefan.schmeisser@lamresearch.com'
    text_content = """
    %s created the part %s.
    Move the attached query to the folder with the bat file and double click it.

    Thanks,
    Lam Part Predictor Team
    """ % (name, part.part)
    html_content = " %s created the part %s.<br> Move the attached query to the folder with the bat file and double click it.<p>Thanks,<br>Lam Part Predictor Team" % (part.name, part.part)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(os.path.join(query_path, id_num + "-" + str(datetime.now().date()) + '.sql'))
    connection = mail.get_connection()
    start_new_thread(connection.send_messages, ([msg],))
    return

    
