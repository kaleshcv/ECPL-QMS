from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .models import *

from . import forms
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

def index(request):
    return render(request,'index.html')

#Guidelines
def outboundGuidelines(request):
    return render(request,'guidelines/outbound.html')
def inboundGuidelines(request):
    return render(request,'guidelines/inbound.html')
def chatGuidelines(request):
    return render(request,'guidelines/chat.html')
def emailGuidelines(request):
    return render(request,'guidelines/email.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # form to create user
        profile_form = forms.ProfileCreation(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # login(request,user)
            return render(request,'index.html')
    else:
        form = UserCreationForm()
        profile_form = forms.ProfileCreation()

    return render(request, 'sign-up.html', {'form': form, 'profile_form': profile_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Login form
        if form.is_valid():
            # login the user
            user = form.get_user()
            login(request, user)
            # redirecting

            if user.profile.emp_desi=='QA':
                return redirect('/employees/qahome')

            else:
                return redirect('/employees/agenthome')
        else:
            form = AuthenticationForm()
            messages.info(request,'Invalid Credentials !')
            return render(request,'login.html',{'form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/employees/login')


def agenthome(request):

    agent_name = request.user.profile.emp_name
    team_name=request.user.profile.team
    team = Team.objects.get(name=team_name)

    # Chat Eva Details
    open_eva_chat=ChatMonitoringFormEva.objects.filter(associate_name=agent_name, status=False)
    open_eva_count = ChatMonitoringFormEva.objects.filter(associate_name=agent_name, status=False).count()

    # Pod Father Chat Details
    open_pod_chat = ChatMonitoringFormPodFather.objects.filter(associate_name=agent_name, status=False)
    open_pod_count = ChatMonitoringFormPodFather.objects.filter(associate_name=agent_name, status=False).count()


    data={'team':team,
          'open_eva_chat':open_eva_chat,'open_eva_count':open_eva_count,
          'open_pod_chat':open_pod_chat,'open_pod_count':open_pod_count,
          }

    return render(request, 'agent-home.html',data)

# Coaching View ---------------------------- !!!

def empCoachingViewEvachat(request,pk):
    coaching=ChatMonitoringFormEva.objects.get(id=pk)
    data={'coaching':coaching}
    return render(request,'emp-coaching-view-eva-chat.html',data)

def qaCoachingViewEvachat(request,pk):
    coaching = ChatMonitoringFormEva.objects.get(id=pk)
    data = {'coaching': coaching}
    return render(request, 'qa-coaching-view-eva-chat.html', data)

def empCoachingViewPodchat(request,pk):
    coaching=ChatMonitoringFormPodFather.objects.get(id=pk)
    data={'coaching':coaching}
    return render(request,'emp-coaching-view-pod-chat.html',data)

def qaCoachingViewPodchat(request,pk):
    coaching = ChatMonitoringFormPodFather.objects.get(id=pk)
    data = {'coaching': coaching}
    return render(request, 'qa-coaching-view-pod-chat.html', data)


def signCoaching(request,pk):
    now = datetime.now()
    category=request.POST['category']
    emp_comments=request.POST['emp_comments']

    if category == 'eva-chat':
        coaching=ChatMonitoringFormEva.objects.get(id=pk)
        coaching.status=True
        coaching.closed_date=now
        coaching.emp_comments=emp_comments
        coaching.save()
        return redirect('/employees/agenthome')
    else:
        pass


def coachingSuccess(request):

    return render(request,'coaching-success-message.html')

def coachingDispute(request):
    if request.method == 'POST':

        team= request.user.profile.team

        team=Team.objects.get(name=team)
        data={'team':team}
        return render(request,'coaching-dispute-message.html',data)
    else:
        return redirect('/employees/agenthome')

def qahome(request):

    qa_name=request.user.profile.emp_name
    user_id=request.user.id
    teams=Team.objects.filter(qa=user_id)

    open_eva_chat=ChatMonitoringFormEva.objects.filter(added_by=qa_name,status=False)
    open_eva_count = ChatMonitoringFormEva.objects.filter(added_by=qa_name,status=False).count()


    data={'teams':teams,'open_eva_chat':open_eva_chat,'open_eva_count':open_eva_count
          }

    return render(request,'qa-home.html',data)


# Final Forms

def chatCoachingformEva(request):
    if request.method == 'POST':

        associate_name = request.POST['empname']
        emp_id = request.POST['empid']
        qa = request.POST['qa']
        team_lead = request.POST['tl']
        ticket_no=request.POST['ticketnumber']
        trans_date = request.POST['transdate']
        audit_date = request.POST['auditdate']
        campaign = request.POST['campaign']
        concept = request.POST['concept']
        evaluator=request.POST['evaluator']

        # Customer Experience
        ce_1 = int(request.POST['ce_1'])
        ce_2 = int(request.POST['ce_2'])
        ce_3 = int(request.POST['ce_3'])
        ce_4 = int(request.POST['ce_4'])

        ce_total=ce_1+ce_2+ce_3+ce_4

        #Compliance
        compliance_1 = int(request.POST['compliance_1'])
        compliance_2 = int(request.POST['compliance_2'])
        compliance_3 = int(request.POST['compliance_3'])
        compliance_4 = int(request.POST['compliance_4'])
        compliance_5 = int(request.POST['compliance_5'])
        compliance_6 = int(request.POST['compliance_6'])

        compliance_total=compliance_1+compliance_2+compliance_3+compliance_4+compliance_5+compliance_6

        if compliance_1==0 or compliance_2==0 or compliance_3==0 or compliance_4==0 or compliance_5==0 or compliance_6==0:
            overall_score=0
        else:
            overall_score=ce_total+compliance_total

        areas_improvement = request.POST['areaimprovement']
        positives = request.POST['positives']
        comments = request.POST['comments']
        added_by = request.user.profile.emp_name

        chat = ChatMonitoringFormEva(associate_name=associate_name, emp_id=emp_id, qa=qa, team_lead=team_lead,

                                     trans_date=trans_date, audit_date=audit_date,ticket_no=ticket_no,
                                     campaign=campaign,concept=concept,evaluator=evaluator,

                                     ce_1=ce_1,ce_2=ce_2,ce_3=ce_3,ce_4=ce_4,ce_total=ce_total,

                                     compliance_1=compliance_1,compliance_2=compliance_2,compliance_3=compliance_3,
                                     compliance_4=compliance_4,compliance_5=compliance_5,compliance_6=compliance_6,
                                     compliance_total=compliance_total,

                                     areas_improvement=areas_improvement,
                                     positives=positives, comments=comments,
                                     added_by=added_by,

                                     overall_score=overall_score
                                     )
        chat.save()
        return redirect('/employees/qahome')
    else:
        teams = Team.objects.all()
        users = User.objects.all()
        data = {'teams': teams, 'users': users}
        return render(request, 'mon-forms/ECPL-EVA&NOVO-Monitoring-Form-chat.html', data)

def chatCoachingformPodFather(request):
    if request.method == 'POST':

        associate_name = request.POST['empname']
        emp_id = request.POST['empid']
        qa = request.POST['qa']
        team_lead = request.POST['tl']
        ticket_no=request.POST['ticketnumber']
        trans_date = request.POST['transdate']
        audit_date = request.POST['auditdate']
        campaign = request.POST['campaign']
        concept = request.POST['concept']
        evaluator=request.POST['evaluator']

        # Customer Experience
        ce_1 = int(request.POST['ce_1'])
        ce_2 = int(request.POST['ce_2'])
        ce_3 = int(request.POST['ce_3'])
        ce_4 = int(request.POST['ce_4'])

        ce_total=ce_1+ce_2+ce_3+ce_4

        #Compliance
        compliance_1 = int(request.POST['compliance_1'])
        compliance_2 = int(request.POST['compliance_2'])
        compliance_3 = int(request.POST['compliance_3'])
        compliance_4 = int(request.POST['compliance_4'])
        compliance_5 = int(request.POST['compliance_5'])
        compliance_6 = int(request.POST['compliance_6'])

        compliance_total=compliance_1+compliance_2+compliance_3+compliance_4+compliance_5+compliance_6

        if compliance_1==0 or compliance_2==0 or compliance_3==0 or compliance_4==0 or compliance_5==0 or compliance_6==0:
            overall_score=0
        else:
            overall_score=ce_total+compliance_total

        areas_improvement = request.POST['areaimprovement']
        positives = request.POST['positives']
        comments = request.POST['comments']
        added_by = request.user.profile.emp_name

        chat = ChatMonitoringFormPodFather(associate_name=associate_name, emp_id=emp_id, qa=qa, team_lead=team_lead,

                                     trans_date=trans_date, audit_date=audit_date,ticket_no=ticket_no,
                                     campaign=campaign,concept=concept,evaluator=evaluator,

                                     ce_1=ce_1,ce_2=ce_2,ce_3=ce_3,ce_4=ce_4,ce_total=ce_total,

                                     compliance_1=compliance_1,compliance_2=compliance_2,compliance_3=compliance_3,
                                     compliance_4=compliance_4,compliance_5=compliance_5,compliance_6=compliance_6,
                                     compliance_total=compliance_total,

                                     areas_improvement=areas_improvement,
                                     positives=positives, comments=comments,
                                     added_by=added_by,

                                     overall_score=overall_score
                                     )
        chat.save()
        return redirect('/employees/qahome')
    else:
        teams = Team.objects.all()
        users = User.objects.all()
        data = {'teams': teams, 'users': users}
        return render(request,'mon-forms/ECPL-Pod-Father-Monitoring-Form-chat.html', data)

def inboundCoachingForm(request):
    if request.method == 'POST':
        associate_name = request.POST['empname']
        emp_id = request.POST['empid']
        qa = request.POST['qa']
        team_lead = request.POST['tl']
        customer_name=request.POST['customer']
        customer_contact=request.POST['customercontact']
        call_date = request.POST['calldate']
        audit_date = request.POST['auditdate']
        campaign = request.POST['campaign']
        concept = request.POST['concept']
        zone=request.POST['zone']
        call_duration=request.POST['duration']

        # Customer Experience
        ce_1 = int(request.POST['ce_1'])
        ce_2 = int(request.POST['ce_2'])
        ce_3 = int(request.POST['ce_3'])
        ce_4 = int(request.POST['ce_4'])
        ce_5 = int(request.POST['ce_5'])
        ce_6 = int(request.POST['ce_6'])
        ce_7 = int(request.POST['ce_7'])
        ce_8 = int(request.POST['ce_8'])
        ce_9 = int(request.POST['ce_9'])
        ce_10 = int(request.POST['ce_10'])
        ce_11 = int(request.POST['ce_11'])

        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        # Business
        business_1 = int(request.POST['business_1'])
        business_2 = int(request.POST['business_2'])

        business_total = business_1 + business_2

        # Compliance
        compliance_1 = int(request.POST['compliance_1'])
        compliance_2 = int(request.POST['compliance_2'])
        compliance_3 = int(request.POST['compliance_3'])

        compliance_total = compliance_1 + compliance_2 + compliance_3

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0:
            overall_score = 0
        else:
            overall_score = ce_total + business_total +compliance_total

        areas_improvement = request.POST['areaimprovement']
        positives = request.POST['positives']
        comments = request.POST['comments']
        added_by = request.user.profile.emp_name

        inbound = InboundMonitoringForm(associate_name=associate_name, emp_id=emp_id, qa=qa, team_lead=team_lead,

                                           call_date=call_date, audit_date=audit_date, customer_name=customer_name,customer_contact=customer_contact,
                                           campaign=campaign, concept=concept, zone=zone,call_duration=call_duration,

                                           ce_1=ce_1, ce_2=ce_2, ce_3=ce_3, ce_4=ce_4, ce_5=ce_5, ce_6=ce_6, ce_7=ce_7, ce_8=ce_8, ce_9=ce_9, ce_10=ce_10, ce_11=ce_11,
                                           ce_total=ce_total,

                                           business_1=business_1,business_2=business_2,business_total=business_total,

                                           compliance_1=compliance_1, compliance_2=compliance_2,compliance_3=compliance_3,compliance_total=compliance_total,

                                           areas_improvement=areas_improvement,
                                           positives=positives, comments=comments,
                                           added_by=added_by,

                                           overall_score=overall_score
                                           )
        inbound.save()
        return redirect('/employees/qahome')
    else:
        teams = Team.objects.all()
        users = User.objects.all()
        data = {'teams': teams, 'users': users}
        return render(request, 'mon-forms/ECPL-INBOUND-CALL-MONITORING-FORM.html', data)



#campaign View

def campaignView(request,pk):
    team=Team.objects.get(id=pk)
    team_name=team.name
    agents=Profile.objects.filter(team=team_name,emp_desi='CRO')

    data = {'team': team,'agents':agents}
    return render(request,'campaign-view.html',data)

def selectCoachingForm(request):
    if request.method == 'POST':
        audit_form=request.POST['audit_form']
        agent=request.POST['agent']
        team=request.POST['team']

        if audit_form=='eva-chat':
            agent=Profile.objects.get(emp_name=agent)
            team=Team.objects.get(name=team)
            data = {'agent':agent,'team':team}
            return render(request, 'mon-forms/ECPL-EVA&NOVO-Monitoring-Form-chat.html', data)
        elif audit_form=='pod-chat':
            agent = Profile.objects.get(emp_name=agent)
            team = Team.objects.get(name=team)
            data = {'agent': agent, 'team': team}
            return render(request, 'mon-forms/ECPL-Pod-Father-Monitoring-Form-chat.html', data)
        elif audit_form=='inbound-call':
            agent = Profile.objects.get(emp_name=agent)
            team = Team.objects.get(name=team)
            data = {'agent': agent, 'team': team}
            return render(request, 'mon-forms/ECPL-INBOUND-CALL-MONITORING-FORM.html', data)

    else:
        pass

def coachingSummaryView(request):
    return render(request,'coaching-summary-view.html')


