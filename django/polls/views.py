from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
import datetime

from .models import Choice, Question



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def log_in(request):
    #FIX ME:
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            return render(request, 'polls/error.html')
        
        if user:
            #check if user has access (field in model class)
            try:
                userobj = User.objects.get(username=username)

            except:
              return redirect('polls:index', {
                'status': "Username already exists", 
                'user': user
                })

                # render(request, 'polls/index.html', {
                # 'status': "Username already exists", 
                # 'user': user
                # })
        return redirect('polls:index')
        # return render(request, 'polls/index.html')
        # return HttpResponseRedirect('/django/nt7ab/polls/index.html')

    return redirect('polls:index')
    # return render(request, 'polls/index.html')
    # return HttpResponseRedirect('/django/nt7ab/polls/index.html')



def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        # return HttpResponseRedirect('/django/nt7ab/polls/index.html')
        # return render(request, 'polls/index.html')
        return redirect('polls:index')
    else:
        # return HttpResponseRedirect('/django/nt7ab/polls/index.html')
        # return render(request, 'polls/index.html')
        return redirect('polls:index')



def add_poll(request):
    if request.user.is_authenticated():
        # return redirect(' polls:add_poll ')
        return render(request, "polls/add_poll.html")
        # return HttpResponseRedirect('/django/nt7ab/polls/add_poll.html')
    else:
        return render(request, 'polls/error.html')
        # return HttpResponseRedirect('/django/nt7ab/polls/error.html')


def add_poll2(request):
    print("In add poll 2")

    if request.user.is_authenticated():
        cur_user = request.user.id

        try:
            user = User.objects.get(id=cur_user)
        except:
            print("User does not exist")

        if request.method == 'POST':
            question_text = request.POST.get('poll_question')
            poll_choices = request.POST.get('poll_choices')
            poll_choices = poll_choices.split(",")

            try:
                question = Question(question_text = question_text, 
                                    question_owner = user,
                                    pub_date = datetime.datetime.now())
                question.save()

                for item in poll_choices:
                    choice = Choice(question=question, choice_text=item)
                    choice.save()

            except Exception as e:
                print(e.message, type(e))
                # return render(request, 'polls/index.html')
                return redirect('polls:index')
                # return HttpResponseRedirect('/django/nt7ab/polls/index.html')

        # return render(request, "polls/index.html")
        return redirect('polls:index')
        # return HttpResponseRedirect('/django/nt7ab/polls/index.html')


def delete_poll(request):
    print ("I'm in DELETE POLL -----------")

    if request.user.is_authenticated():
        poll_id = request.POST.get('poll_id')

        try: 
            ques = Question.objects.get(pk = poll_id)
        except:
            return render(request, 'polls/error.html')

        # print(str(request.user.username), str(ques.question_owner), poll_id, ques)

        if (str(request.user.username) == str(ques.question_owner)):
            ques.delete()
        else:
            return render(request, 'polls/error.html')
            # return HttpResponseRedirect('/django/nt7ab/polls/error.html')

    else:
        return render(request, 'polls/error.html')
        # return HttpResponseRedirect('/django/nt7ab/polls/error.html')

    return render(request, 'polls/index.html')
    # return redirect('polls:index')
    # return HttpResponseRedirect('/django/nt7ab/polls/index.html')



def add_user(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        return render(request, 'polls/add_user.html')
        # return redirect('polls:add_user')
        # return HttpResponseRedirect('/django/nt7ab/polls/add_user.html')
    else:
        return render(request, 'polls/error.html')
        # return HttpResponseRedirect('/django/nt7ab/polls/error.html')


def add_user2(request):
    print("I'm in ADD USER2")

    if (request.method == 'POST') and (request.user.is_authenticated()) and request.user.is_superuser:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')


        if (user_type == "admin"):
            is_superuser = True
        else:
            is_superuser = False

        try: 
            user = User(username = username, password = password, is_superuser = is_superuser)
            user.set_password(password)
            user.save()
        except:
            # return render(request, 'polls/index.html', {'status': "Username already exists"})
            return redirect('polls:index')
            # return HttpResponseRedirect('/django/nt7ab/polls/index.html')

    else:
        # return HttpResponseRedirect('/django/nt7ab/polls/index.html')
        return redirect('polls:index')
        # render(request, 'polls/index.html', {'status': "You're not an admin user, cannot create new users"})
    # return render(request, 'polls/index.html')
    return redirect('polls:index')
    # return HttpResponseRedirect('/django/nt7ab/polls/index.html')



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
	    """
	    Return the last five published questions (not including those set to be
	    published in the future).
	    """
	    return Question.objects.filter(
	        pub_date__lte=timezone.now()
	    ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
