from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No has seleccionado una opcion de la encuesta.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def question_view(request):
    if request.method == "POST":
       form = QuestionForm(request.POST)
       if form.is_valid():
          form.save()
          return render(request, "polls/success.html")
    else:
        form = QuestionForm()
    return render(request, 'polls/question_form.html', {'form': form})
def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'polls/success.html')
    else:
        form = QuestionForm()
    
    return render(request, 'polls/question_form.html', {'form': form})
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question  
            choice.save()
            return render(request, 'polls/success_choice.html', {'question': question, 'choice': choice})
    else:
        form = ChoiceForm()
    return render(request, 'polls/add_choice.html', {'form': form, 'question': question})