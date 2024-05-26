from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from .models import Choice, Question

# Class for creating the index view
class IndexView(LoginRequiredMixin, generic.ListView): #Added a parameter "LoginRequiredMixin" that checks that the user is logged in
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # Function that returns the last five published questions
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# Class for creating the detail view
@method_decorator(csrf_protect, name="dispatch")
class DetailView(LoginRequiredMixin, generic.DetailView): #Added a parameter "LoginRequiredMixin" that checks that the user is logged in
    model = Question
    template_name = 'polls/detail.html'

# Class for creating the results view
@method_decorator(csrf_protect, name="dispatch")
class ResultsView(LoginRequiredMixin, generic.DetailView): #Added a parameter "LoginRequiredMixin" that checks that the user is logged in
    model = Question
    template_name = 'polls/results.html'

    # Function that checks if a user has voted before accessing the results
    # This function should be uncommented to fix flaw #2! (see line 51 also)
    """def get(self, request, *args, **kwargs):
        if not request.session.get('can_view_results'):
            raise Http404("Results cannot be accessed directly.")
        request.session['can_view_results'] = False  # Reset the flag
        return super().get(request, *args, **kwargs)"""

# Function that allows the user to vote in a poll
@login_required
#Uncomment @csrf_protect to fix flaw #1!
#@csrf_protect
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # The code under this line should be uncommented to fix flaw #2!
        #request.session['can_view_results'] = True  # Set the flag for the get() function
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))