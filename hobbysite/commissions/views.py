from django.shortcuts import render, redirect
from .models import Commission, JobApplication, Job
from django.db.models import Case, When, IntegerField, Value
from django.contrib.auth.decorators import login_required
from .forms import CommissionForm, JobForm


def commissions_list(request):
    commissions = Commission.objects.annotate(
        status_order = Case(
            When(status = 'Open', then=Value(0)),
            When(status = 'Full', then=Value(1)),
            When(status = 'Completed', then=Value(2)),
            When(status = 'Discontinued', then=Value(3)),
            output_field=IntegerField()
        )
    ).order_by('status_order', '-created_on')

    created_commissions = []
    applied_commissions = []

    if request.user.is_authenticated:
        created_commissions = Commission.objects.filter(author=request.user)
        applicant_id = JobApplication.objects.filter(applicant=request.user).values_list('job__commission', flat=True)
        applied_commissions = Commission.objects.filter(id__in = applicant_id)
    ctx = {
            'created_commissions': created_commissions,
            'applied_commissions': applied_commissions,
            'commissions': commissions
    }
    return render(request, 'commissions_list.html', ctx)
    
def commissions_detail(request, id):
    commission = Commission.objects.get(id=id)
    jobs = Job.objects.filter(commission=commission)
    
    total_mp = sum(job.manpower_required for job in jobs)
    total_accepted = sum(JobApplication.objects.filter(job=job, status = '1').count() for job in jobs)
    open_mp = total_mp - total_accepted

    is_owner = request.user.is_authenticated and commission.author == request.user
    full_jobs = []
    
    for job in jobs:
        jobs_accepted = JobApplication.objects.filter(job=job, status = '1').count()
        if jobs_accepted >= job.manpower_required:
            full_jobs.append(job)

    ctx = { 
        'commission': commission,
        'jobs': jobs,
        'total_mp': total_mp,
        'open_mp': open_mp,
        'is_owner': is_owner,
        'full_jobs': full_jobs
        }
    return render(request, 'commissions_detail.html', ctx)

@login_required
def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        if not JobApplication.objects.filter(job=job, applicant = request.user).exists():
            JobApplication.objects.create(job=job, applicant=request.user, status='0')
            return redirect('commissions:commissions_detail', id=job.commission.id)
    return redirect('commissions:commissions_detail', id=job.commission.id)

@login_required
def create_view(request):
    form = CommissionForm()
    if request.method == 'POST':
        form = CommissionForm(request.POST)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.author = request.user
            commission.save()
            return redirect('commissions:commissions_detail', id=commission.id)
    
    ctx = { 'form': form}
    return render(request, 'create_commission.html', ctx)

@login_required
def update_view(request, id):
    commission = Commission.objects.get(id=id)
    if commission.author != request.user:
        return redirect('commissions:commissions_list')
    
    if request.method == 'POST':
        form = CommissionForm(request.POST, instance=commission)
        if form.is_valid():
            form.save()

            jobs = Job.objects.filter(commission=commission)
            jobs_full = all(JobApplication.objects.filter(job=job, status='1').count() >= job.manpower_required for job in jobs)

            if jobs_full and jobs.exists():
                commission.status = 'Full'
            commission.save()
            return redirect('commissions:commissions_detail', id=commission.id)
    else:
        form = CommissionForm(instance=commission)
    
    ctx = { 'form': form, 'commission':commission}
    return render(request, 'update_commission.html', ctx)

@login_required
def job_view(request, job_id):
    job = Job.objects.get(id=job_id)
    applicants = JobApplication.objects.filter(job=job)
    is_owner = request.user == job.commission.author

    if request.method == 'POST' and is_owner:
        choice = request.POST.get('choice')
        applicant_id = request.POST.get('applicant_id')
        job_application = JobApplication.objects.get(id=applicant_id)

        if choice == 'accept':
            job_application.status = '1'
        elif choice == 'reject':
            job_application.status = '2'
        job_application.save()

        return redirect('commissions:job_view', job_id=job.id)
    
    ctx = {
        'job': job,
        'is_owner': is_owner,
        'applicants': applicants,
    }

    return render(request, 'job.html', ctx)

@login_required
def create_job(request, commission_id):
    commission = Commission.objects.get(id=commission_id)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.commission = commission
            job.save()
            return redirect('commissions:commissions_detail', id=commission.id)
    else: 
        form = JobForm()
        
    
    ctx = { 'form': form}
    return render(request, 'create_job.html', ctx)
    


