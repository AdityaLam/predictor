from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import FileForm

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            write_file(form.cleaned_data['filename'], request.FILES['csv'])
            return HttpResponseRedirect('upload/success/')
    else:
        form = FileForm()
    return render(request, 'upload/upload.html', {'form': form})

def write_file(name, f):
    with open(name +'.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def success(request):
    return HttpResponse("gg wp")
