from django.shortcuts import render
from .models import Commission

def commissions_list(request):
    commissions = Commission.objects.all()
    ctx = {'commissions': commissions}
    return render(request, 'commissions_list.html', ctx)

def commissions_detail(request, id):
    ctx = { 'commission': Commission.objects.get(id=id)}
    return render(request, 'commissions_detail.html', ctx)
