from django.shortcuts import render, get_object_or_404, redirect

from website.forms import PenduForm


# Create your views here.

def index(request):
    return render(request,"website/index.html")

def pendu(request):
    guess_word = "carambar"
    guess_word_length = len(guess_word)
    word_letters = list(guess_word)

    on_game = True
    while on_game:
        if request.method == 'POST':
            game_started = True
            form = PenduForm(request.POST)
            if form.is_valid():
                user_letter = form.cleaned_data["letter"]
                letter_state = False

                index = []

                for i,letter in enumerate(word_letters):

                    if user_letter == letter:
                        letter_state = True
                        index.append(i)
                        on_game = False


                    else:
                        letter_state = False


                context = {"form":form, "userLetter":user_letter,"letter_state":letter_state, "guess_word":guess_word, "word_letters":word_letters, "index":index}
                return render(request, "pendu/index.html", context)
        else:
            form = PenduForm()

        context = {"form": form}
        return render(request,"pendu/index.html", context)
    return render(request,"pendu/win.html")