from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import mail
from django.core.mail import EmailMultiAlternatives
import os
from _thread import start_new_thread
from .models import Person, Part

script_dir = os.path.dirname(__file__)
rel_data = "../files/yesterday/data.csv"
data_path = os.path.join(script_dir, rel_data)

@csrf_exempt
def upload(request):
    import csv
    if request.method == 'POST':
        data = request.FILES['data']
        write_file(data)
        with open(data_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            messages = []
            for row in reader:
                if len(row) == 4:
                    p = Person.objects.filter(uid = row[3].strip()).first()
                    if p:
                        part = Part.create(p, row[0])
                        part.save()
                        subject, from_email, to = 'Part Predictor', 'lampredictor@gmail.com', part.email
                        text_content = """
                        Thanks for entering in the part %s.
                        Please click or enter this link to fill out the part form:
                        http://104.236.134.227/form/%d

                        Thanks,
                        Lam Part Predictor Team
                        """ % (part.part, part.id)
                        html_content = "Thanks for entering in the part %s.<br>Please click or enter this link to fill out the part form:<br><a href = 'http://104.236.134.227/form/%d'>http://104.236.134.227/form/%d</a><p>Thanks,<br>Lam Part Predictor Team" % (part.part, part.id, part.id)
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        messages.append(msg)
            connection = mail.get_connection()
            start_new_thread(connection.send_messages, (messages,))
            return HttpResponse('emails sent')
    else:
        return HttpResponse("hello, you shouldn't be seeing this page, please leave")

def write_file(f):
    with open(data_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)