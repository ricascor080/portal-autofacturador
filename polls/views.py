from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Vote
import csv
from .forms import RegisterForm
from django.utils.dateparse import parse_date


# ============================
# Vistas del tutorial (polls)
# ============================

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Últimas 5 preguntas publicadas (no futuras)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excluye preguntas futuras."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """Versión del tutorial: incrementa votos en Choice (no recomendada si usas Vote)."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    # ⚠️ Esto ya no aplica si trabajas con el modelo Vote
    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# ============================
# Autenticación
# ============================

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("polls:dashboard")

        messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "polls/login.html")



@login_required
def dashboard(request):
    user = request.user
    questions = Question.objects.all()

    if user.is_superuser:
        chart_data = [
            {
                "question_text": q.question_text,
                "total_votes": sum(c.votes_count for c in q.choices.all())
            }
            for q in questions
        ]
        return render(request, "polls/admin_dashboard.html", {
            "questions": questions,
            "chart_data": chart_data,
        })

    return redirect("polls:user_dashboard")


def index(request):
    return redirect("polls:login")


@login_required
def user_dashboard(request):
    questions = Question.objects.all()

    if request.method == "POST":
        question_id = request.POST.get("question_id")
        choice_id = request.POST.get("choice_id")

        if question_id and choice_id:
            question = Question.objects.get(pk=question_id)
            choice = Choice.objects.get(pk=choice_id)

            existing_vote = Vote.objects.filter(user=request.user, question=question).first()
            if existing_vote:
                existing_vote.choice = choice
                existing_vote.save()
            else:
                Vote.objects.create(user=request.user, question=question, choice=choice)

        return redirect("polls:user_dashboard")

    my_votes = Vote.objects.filter(user=request.user).select_related("question", "choice")

    return render(request, "polls/user_dashboard.html", {
        "questions": questions,
        "my_votes": my_votes,
    })


@login_required
def add_question(request):
    if request.method == "POST" and request.user.is_superuser:
        text = request.POST["question_text"]
        Question.objects.create(question_text=text, pub_date=timezone.now())
    return redirect("polls:dashboard")


@login_required
def add_choice(request):
    if request.method == "POST" and request.user.is_superuser:
        q_id = request.POST["question_id"]
        choice_text = request.POST["choice_text"]
        question = get_object_or_404(Question, pk=q_id)
        Choice.objects.create(question=question, choice_text=choice_text)
    return redirect("polls:dashboard")


@login_required
def export_csv(request):
    from_date = parse_date(request.GET.get("from"))
    to_date = parse_date(request.GET.get("to"))

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="reporte.csv"'

    writer = csv.writer(response)
    writer.writerow(["Pregunta", "Opción", "Votos en rango"])

    for choice in Choice.objects.all():
        if from_date and to_date:
            votes_count = Vote.objects.filter(
                choice=choice,
                voted_at__date__range=[from_date, to_date]
            ).count()
        else:
            votes_count = choice.votes_count

        writer.writerow([
            choice.question.question_text,
            choice.choice_text,
            votes_count
        ])

    return response


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("polls:dashboard")
    else:
        form = RegisterForm()
    return render(request, "polls/register.html", {"form": form})
