from django.shortcuts import render, get_object_or_404, redirect

from website.forms import PenduForm


# Create your views here.

def index(request):
    return render(request,"website/index.html")

def pendu(request):
    guess_word = "carambar"
    word_letters = list(guess_word)

    if request.method == 'POST':
        form = PenduForm(request.POST)
        if form.is_valid():
            letter = form.cleaned_data["letter"]
            if letter in word_letters:
                letter_state = "cette lettre est dans le mot"
            else:
                letter_state = "cette lettre n'est pas dans le mot"
            context = {"form":form, "userLetter":letter,"letter_state":letter_state, "guess_word":guess_word, "word_letters":word_letters}
            return render(request, "pendu/index.html", context)
    else:
        form = PenduForm()

    context = {"form": form}
    return render(request,"pendu/index.html", context)
