# Create your views here.

from dragon.models import Experiment,UserProfile,ApplyRecord,User

from django.template import RequestContext
from django.shortcuts import render_to_response
from dragon.forms import UserForm, UserProfileForm,ExperimentForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    context_dict = {}


    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    try:
        ExperimentList1 = Experiment.objects.filter(isOverdue=True).order_by('-payment')[:5]
        context_dict['experiments1'] = ExperimentList1
        ExperimentList2 = Experiment.objects.filter(isOverdue=True).order_by('-startTime')[:5]
        context_dict['experiments2'] = ExperimentList2
        ExperimentList3 = Experiment.objects.filter(isOverdue=True).order_by('-endTime').reverse()[:5]
        context_dict['experiments3'] = ExperimentList3
    except Experiment.DoesNotExist:
        pass
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('dragon/index.html', context_dict, context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.

    return render_to_response(
        'dragon/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)

def userHome(request):
    return render_to_response(
        'dragon/userHome.html',)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/dragon/Login/userHome')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your dragon account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('dragon/Login.html', {}, context)


def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/dragon/')


def index_search(request):
    context = RequestContext(request)
    result_list = []
    if request.method == 'POST':
      search = request.POST['field1']
      print(search)
      type1 = request.POST['field2']

      if search == "":
          result_list=[]
      else:
        if type1 == 'Payment':
            result_list = Experiment.objects.filter(isOverdue=True,title__icontains=search).order_by(
                '-payment')[:5]
        elif type1 == 'StartTime':
            result_list = Experiment.objects.filter(isOverdue=True,title__icontains=search).order_by(
                '-startTime')[:5]
        elif type1 == 'EndTime':
            result_list = Experiment.objects.filter(isOverdue=True, title__icontains=search).order_by(
                '-endTime').reverse()[:5]

    return render_to_response('dragon/search.html', {'result_list': result_list}, context)

def intro_out(request,offset):
      context = RequestContext(request)
      try:
          offset=int(offset)
      except ValueError:
            raise Http404()
      try:
           result_list=Experiment.objects.get(pk=offset)
           firstName = User.objects.get(username=result_list.userId).first_name
           SecondName = User.objects.get(username=result_list.userId).last_name
      except Experiment.DoesNotExist:
           pass

      return render_to_response('dragon/intro.html', {'result_list': result_list,'firstName': firstName,'secondName':SecondName}, context)
def user_available(request):
    context = RequestContext(request)
    username = request.user.username
    result_list = []
    result_list2 = []
    try:
        user1= User.objects.get(username=username)


        print(user1)
        userProfile = UserProfile.objects.get(user=user1)
        result_list2 = ApplyRecord.objects.filter( applicantId=userProfile,isProcessed=True,isValid=True)

        from django.db.models import Q
        if userProfile.educationLevel == 'PHD':
            result_list =list(Experiment.objects.filter(Q(isOverdue=True),(Q(language=userProfile.firstLanguage)|Q(language= 'Any'))).exclude(userId =userProfile))
        elif userProfile.educationLevel == 'Master':
            result_list = list(Experiment.objects.filter(Q(isOverdue=True),(Q(language=userProfile.firstLanguage)|Q(language= 'Any')),(Q(educationDemand='Master')|Q(educationDemand='Undergraduate'))).exclude(userId=userProfile))
        elif userProfile.educationLevel == 'Postgraduate':
            result_list =list(Experiment.objects.filter(Q(isOverdue=True),(Q(language=userProfile.firstLanguage)|Q(language= 'Any')),Q(educationDemand='Undergraduate')).exclude(userId=userProfile))
        print(result_list)
        if result_list and result_list2:
          for applyRecord1 in result_list2:
            for experiment1 in  result_list:

                if experiment1.title == applyRecord1.experimentId.title:
                            result_list.remove(experiment1)

    except User.DoesNotExist:
        pass

    return render_to_response('dragon/AvailableExperiment.html', {'result_list': result_list}, context)

def user_Apply(request):
      context = RequestContext(request)
      if request.method == 'POST':
        username = request.user.username
        ExperimentTitle = request.POST['ExperimentName']
      try:
        user1= User.objects.get(username=username)
        userProfile = UserProfile.objects.get(user=user1)
        experiment = Experiment.objects.get(title__exact=ExperimentTitle,isOverdue=True)
        p =ApplyRecord(applicantId=userProfile,experimentId=experiment,ApplyTime=datetime.datetime.now())
        p.save()

        return render_to_response('dragon/SuccessfulApply.html',{}, context)
      except Experiment.DoesNotExist:
        return render_to_response('dragon/ErrorApply.html',{}, context)



def intro_login(request,offset):
      context = RequestContext(request)
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
           result_list=Experiment.objects.get(pk=offset)
           firstName = User.objects.get(username=result_list.userId).first_name
           SecondName = User.objects.get(username=result_list.userId).last_name
      except Experiment.DoesNotExist:
           pass

      return render_to_response('dragon/intro_Login.html', {'result_list': result_list,'firstName': firstName,'secondName':SecondName}, context)

def apply_intro_login(request,offset):
      context = RequestContext(request)
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
           result_list=Experiment.objects.get(pk=offset)
           firstName = User.objects.get(username=result_list.userId).first_name
           SecondName = User.objects.get(username=result_list.userId).last_name
      except Experiment.DoesNotExist:
           pass

      return render_to_response('dragon/apply_intro_login.html', {'result_list': result_list,'firstName': firstName,'secondName':SecondName}, context)

def user_info(request):
     context = RequestContext(request)
     result_list=[]
     try:
         result_list=UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
         pass
     return render_to_response('dragon/User_infor.html', {'result_list': result_list}, context)
def user_info1(request,offset):
    context = RequestContext(request)
    result_list=[]
    try:
          offset=int(offset)
    except ValueError:
          raise Http404()
    try:
         result_list=UserProfile.objects.get(id=offset)
    except UserProfile.DoesNotExist:
         pass
    return render_to_response('dragon/User_infor1.html', {'result_list': result_list}, context)


def user_ExperListNow(request):
    context = RequestContext(request)
    username1 = request.user.username
    result_list1=[]

    try:
        user1= User.objects.get(username=username1)
        userProfile = UserProfile.objects.get(user=user1)
        result_list1= Experiment.objects.filter(userId=userProfile,isOverdue=True)


    except User.DoesNotExist:
        pass
    return render_to_response('dragon/ownedList.html',{'result_list1': result_list1},context)

def user_ExperOne(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      applyRecord2=[]
      applyRecord3=[]
      experiment1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
          experiment1=Experiment.objects.get(id=offset)
          applyRecord1=ApplyRecord.objects.filter(experimentId=experiment1,isProcessed=True,isValid=True,isOffered=False,isAccepted=False)
          applyRecord2=ApplyRecord.objects.filter(experimentId=experiment1,isProcessed=True,isValid=True,isOffered=True,isAccepted=False)
          applyRecord3=ApplyRecord.objects.filter(experimentId=experiment1,isValid=True,isOffered=True,isAccepted=True)
      except Experiment.DoesNotExist:
          pass

      return render_to_response('dragon/dealExperiment.html',{'applyRecord1': applyRecord1,'applyRecord2': applyRecord2,'applyRecord3': applyRecord3,'experiment1': experiment1},context)
def user_offer(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
         applyRecord1=ApplyRecord.objects.get(id=offset)
         ApplyRecord.objects.filter(id=offset,isValid=True,isOffered=False,isAccepted=False).update(isOffered=True)
      except ApplyRecord.DoesNotExist:
          pass
      return render_to_response('dragon/offer.html',{'applyRecord': applyRecord1},context)
def user_refuse(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
         applyRecord1=ApplyRecord.objects.get(id=offset)
         ApplyRecord.objects.filter(id=offset,isValid=True,isOffered=False,isAccepted=False).update(isProcessed=False)
      except ApplyRecord.DoesNotExist:
          pass
      return render_to_response('dragon/refuse.html',{'applyRecord': applyRecord1},context)
def user_cancel(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
         applyRecord1=ApplyRecord.objects.get(id=offset)
         ApplyRecord.objects.filter(id=offset,isProcessed=True,isValid=True,isOffered=True,isAccepted=False).update(isOffered=False)
      except ApplyRecord.DoesNotExist:
          pass
      return render_to_response('dragon/cancel.html',{'applyRecord': applyRecord1},context)

def addNewExperiment(request):
    context =RequestContext(request)
    if request.method=='POST':
        form=ExperimentForm(request.POST)

        if form.is_valid():

           experiment=form.save(commit=False)
           try:
               username1=request.user.username
               print(username1)
               user1=User.objects.get(username=username1)
               userProfile=UserProfile.objects.get(user=user1)
               print(userProfile)
               experiment.userId=userProfile
               experiment.save()
           except User.DoesNotExist:
               return register(request)



           return HttpResponseRedirect('/dragon/Login/ownedList')
        else:
           return HttpResponseRedirect('/dragon/Login/addError')
    else:
        form=ExperimentForm()
        return render_to_response('dragon/addExperiment.html',{'form':form},context)

def user_addError(request):

     return render_to_response('dragon/addError.html')

def user_ApplyListNow(request):
    context = RequestContext(request)
    username1 = request.user.username
    result_list1=[]
    result_list2=[]
    result_list3=[]
    try:
        user1= User.objects.get(username=username1)
        userProfile = UserProfile.objects.get(user=user1)
        result_list1=ApplyRecord.objects.filter(applicantId=userProfile,isValid=True,isProcessed=True,isOffered=False,isAccepted=False)
        result_list2=ApplyRecord.objects.filter(applicantId=userProfile,isValid=True,isProcessed=True,isOffered=True,isAccepted=False)
        result_list3=ApplyRecord.objects.filter(applicantId=userProfile,isValid=True,isProcessed=True,isOffered=True,isAccepted=True)
        print(result_list3)

    except User.DoesNotExist:
        pass
    return render_to_response('dragon/applyList.html',{'result_list1': result_list1,'result_list2': result_list2,'result_list3': result_list3},context)

def user_pCancel(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()

      try:
         applyRecord1=ApplyRecord.objects.get(id=offset,isValid=True)
         ApplyRecord.objects.filter(id=offset,isValid=True).update(isProcessed=False)

      except  ApplyRecord.DoesNotExist:
         pass

      return render_to_response('dragon/PendCancel.html',{'applyRecord': applyRecord1},context)
def user_iAccept(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
         applyRecord1=ApplyRecord.objects.get(id=offset,isValid=True)
         number=applyRecord1.experimentId.currentOffer
         currentId=applyRecord1.experimentId.id
         number=number+1
         ApplyRecord.objects.filter(id=offset,isValid=True,isOffered=True).update(isAccepted=True)
         Experiment.objects.filter(id=currentId,isOverdue=True).update(currentOffer=number)
      except  ApplyRecord.DoesNotExist:
         pass
      return render_to_response('dragon/InviteAccept.html',{'applyRecord': applyRecord1},context)



def user_iReject(request,offset):
      context = RequestContext(request)
      applyRecord1=[]
      try:
          offset=int(offset)
      except ValueError:
          raise Http404()
      try:
         applyRecord1=ApplyRecord.objects.get(id=offset,isOffered=True,isValid=True)
         ApplyRecord.objects.filter(id=offset,isValid=True).update(isProcessed=False)

      except  ApplyRecord.DoesNotExist:
         pass
      return render_to_response('dragon/InviteCancel.html',{'applyRecord': applyRecord1},context)
