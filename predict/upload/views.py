from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import FileForm
from yesterday.models import Part
from django.views.decorators.csrf import csrf_exempt
import os
from .utils import *

def form(request):
    form = FileForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            csv = request.FILES['csv']
            write_file(csv)
            summary = analyze()
            erf, rpm = find_count()
            inter = 100
            if rpm > 40 and erf > 30:        
                conf = summary.conf_int(.05) 
                inter = 95
            elif rpm > 30 and erf > 20:        
                conf = summary.conf_int(.1) 
                inter = 90
            elif rpm > 20 and erf > 15:        
                conf = summary.conf_int(.2) 
                inter = 80
            else:        
                conf = summary.conf_int(.4) 
                inter = 60
            return render(request, 'upload/results.html', {'count':erf+rpm, 'inter':inter, 'conf':conf, 'aves':summary.params})

def auto_post(request):
    if request.method == 'POST':
        csv = request.FILES['csv']
        id_num = clean_file(csv)
         p = Person.objects.filter(id = id_num).first()
        if p:
            script_dir = os.path.dirname(__file__)
            rel_data = "../static/plot.png"
            img_path = os.path.join(script_dir, rel_data)
            summary = analyze()
            erf, rpm = find_count()
            inter = 100
            if rpm > 40 and erf > 30:        
                conf = summary.conf_int(.05) 
                inter = 95
            elif rpm > 30 and erf > 20:        
                conf = summary.conf_int(.1) 
                inter = 90
            elif rpm > 20 and erf > 15:        
                conf = summary.conf_int(.2) 
                inter = 80
            else:        
                conf = summary.conf_int(.4) 
                inter = 60
            subject, from_email, to = 'Part Predictor', 'lampredictor@gmail.com', p.email
            text_content = """
            Based on the mutiple regression tests, we are %d percent certain that this part will come between %.2f and %.2f  days, with an average of %.2f days.
            If this order is an ERF, it will take between %.2f  and %.2f more days, with an average of %.2f days.
            Based on %d data points.
            Attached is a box plot of all the data we have on the part number specified.

            Thanks,
            Lam Part Predictor Team
            """ % (inter, conf[0][0], conf [1][0], summary.params[0], conf[0][1], conf[1],[1], summary.params[1], rpm+erf)
            html_content = "Based on the mutiple regression tests, we are %d percent certain that this part will come between %.2f and %.2f  days, with an average of %.2f days. <br> If this order is an ERF, it will take between %.2f  and %.2f more days, with an average of %.2f days.<br>Based on %d data points. <br> Attached is a box plot of all the data we have on the part number specified.<p> Thanks,<br>Lam Part Predictor Team"  % (inter, conf[0][0], conf [1][0], summary.params[0], conf[0][1], conf[1],[1], summary.params[1], rpm+erf)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.attach_file(img_path)
            connection = mail.get_connection()
            start_new_thread(connection.send_messages, ([msg],))
            return HttpResponse('results sent')
        else:
            return HttpResponse('error in finding person')
        
script_dir = os.path.dirname(__file__)
rel_data = "../files/upload/data.csv"
data_path = os.path.join(script_dir, rel_data)

def write_file(f):
    with open(data_path, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def clean_file(f):
    import csv
    write_file(f)
    f = open(temp_path, "r+w")
    lines=f.readlines()
    lines, id_num = lines[:-1], lines[-1][0]

    cWriter = csv.writer(f, delimiter=',')
    for line in lines:
        cWriter.writerow(line)
    return id_num

def success(request):
    return HttpResponse("gg wp")
 