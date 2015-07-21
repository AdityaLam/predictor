from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

@csrf_exempt
def upload(request):
    import csv
    if request.method == 'POST':
        data = request.FILES['data']
        filename = 'data.csv'
        write_file(filename, data)
        with open('data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[3] in emails:
                    body = """a;sdklfjasld
                              Thanks, your og homies at LAM
                           """
                    email = EmailMessage('Part Form', body, emails[row[3]])
                    email.attach_file('/folder/name.csv')
                    email.send()
            return HttpResponse()
    else:
        return HttpResponse("hello, you shouldn't be seeing this page, please leave")

def write_file(name, f):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)