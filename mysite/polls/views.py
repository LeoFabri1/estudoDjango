from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView
from .models import Choice, Question
from pathlib import Path


class IndexView(ListView):
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

    def get_template_names(self):
        template_path = str(Path(__file__).resolve().parent / 'templates' / 'polls' / 'index.html')
        return [template_path]


class DetailView(generic.DetailView):
    model = Question

    def get_template_names(self):
        template_path = str(Path(__file__).resolve().parent / 'templates' / 'polls' / 'detail.html')
        return [template_path]


class ResultsView(generic.ListView):
    model = Choice
    context_object_name = "choices"

    def get_queryset(self):
        question_id = self.kwargs["pk"]
        return Choice.objects.filter(question_id=question_id)

    def get_template_names(self):
        template_path = str(Path(__file__).resolve().parent / 'templates' / 'polls' / 'results.html')
        #test
        print("ResultsView called")
        return [template_path]


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = Choice.objects.get(pk=request.POST["choice"], question=question)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        template_path = str(Path(__file__).resolve().parent / 'templates' / 'polls' / 'detail.html')
        return render(request, template_path, {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save(update_fields=["votes"])
        #test
        print(f"Vote recorded: {selected_choice.choice_text} - {selected_choice.votes}")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
