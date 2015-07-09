from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import FileForm
from .utils import *

def form(request):
    form = FileForm()
    return render(request, 'upload/upload.html', {'form': form})


def upload(request):
    if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                filename = 'files/' + form.cleaned_data['filename'] +'.csv' 
                csv = request.FILES['csv']
                write_file(filename, csv)
                summary = analyze(filename)
                conf = summary.conf_int() 
                time_min = conf[0][0]
                time_ave = summary.params[0]
                time_max = conf[1][0]
                erf_min = conf[0][1]
                erf_ave = summary.params[1]
                erf_max = conf[1][1]
                return render(request, 'upload/results.html',
                     {'tmin': time_min, 'tave': time_ave, 'tmax': time_max, 
                     'emin': erf_min, 'eave': erf_ave, 'emax': erf_max})

def write_file(name, f):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def success(request):
    return HttpResponse("gg wp")
 