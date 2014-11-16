from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import RegisterForm, EditAccountForm, ChangeEmailForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required

from accounts.models import Account


def register(request):
    if request.method == "POST":
        nextPage = request.POST.get("next", "/")
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                print "Unable to save form..."
                return render_to_response("registration/registration.html", {'form': form, 'next': nextPage}, context_instance=RequestContext(request))
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password1"))
            login(request, user)
            account = Account()
            account.user = User.objects.get(pk=user.id)
            account.created_by = user
            account.save()
            return redirect(nextPage)
        else:
            print "errors in registration"
            print form.errors
    else:
        form = RegisterForm()
        nextPage = request.GET.get("next", "/")
    # return render_to_response("registration/login.html", {}, context_instance=RequestContext(request))
    return redirect("ig.api.connectInstagram")


def create_account(user):
    try:
        account = Account.objects.get(user=user)
        # print "Account already exists"
    except:
        account = Account()
        account.user = User.objects.get(pk=user.id)
        account.created_by = user
        try:
            account.save()
            return True
        except Exception as e:
            print "Unable to save account..."
            print e
            return False
    return True


def login_func(request):
    nextPage = request.GET.get("next", "/")
    state = ""
    stateStatus = ""
    if request.method == "POST":
        nextPage = request.POST.get("next", "/")
        try:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        state = "You're successfully logged in!"
                        try:
                            create_account(user)
                        except Exception, e:
                            print "Unable to create account"
                            print e
                    else:
                        state = "Your account is not active, please contact the site administrator"
                else:
                    state = "Your username and/or password were incorrect."
                login(request, user)
                return redirect(nextPage)
            else:
                state = "Your username and/or password were incorrect."
                return render_to_response("registration/login.html", {'a_form': form, 'next': nextPage, 'state': state}, context_instance=RequestContext(request))
        except Exception as e:
            print "Error authenticating form"
            print e
    else:
        form = AuthenticationForm()

    #return render_to_response("registration/login.html", {'a_form': form, 'next': nextPage, 'state': state}, context_instance=RequestContext(request))
    return redirect("instagram.api.connectInstagram")