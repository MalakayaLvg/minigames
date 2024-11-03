from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

from website.forms import PenduForm


# Create your views here.

def index(request):
    return render(request,"website/index.html")

def pendu_start(request):

    request.session['user_letters_guessed'] = 0
    request.session['user_letters_try'] = []


def pendu(request):
    guess_word = "carambar"
    guess_word_length = len(guess_word)
    guess_word_letters = list(guess_word)
    user_letters_guessed = request.session.get("user_letters_guessed",0)
    user_letters_try = request.session.get("user_letters_try",[])

    # print(user_letters_try)

    if request.method == 'POST':

        form = PenduForm(request.POST)
        if form.is_valid():
            user_letter = form.cleaned_data["letter"]
            letter_state = False
            index = []
            # print(user_letters_try)
            ############### Lettre deja tenté ?
            if user_letter in user_letters_try:
                print("deja tenté")

            else:
                # print("lettre valable")

                ################ STATE

                if user_letter in guess_word_letters:
                    letter_state = True
                    user_letters_try.append(user_letter)
                    request.session["user_letters_try"] = user_letters_try
                else:
                    letter_state = False

                ############ boucle lettre
                for i, letter in enumerate(guess_word_letters):
                    # print(i)
                    if user_letter == letter:
                        # print(letter)
                        index.append(i)
                        user_letters_guessed += 1
                        request.session["user_letters_guessed"] = user_letters_guessed
                        print(user_letters_guessed)

                ############# WIN CONDITION
                # print(user_letters_guessed)
                print(guess_word_length)
                if user_letters_guessed == guess_word_length:
                    return render(request,"pendu/win.html")

            context = {"form": form, "userLetter": user_letter, "letter_state": letter_state,
                       "guess_word": guess_word, "guess_word_letters": guess_word_letters, "index": index,
                       "user_letters_guessed": user_letters_guessed}
            return render(request, "pendu/index.html", context)


    else:
        form = PenduForm()

    context = {"form": form}
    return render(request,"pendu/index.html", context)

def pendu_reset(request):
    request.session.pop("user_letters_guessed",None)
    request.session.pop("user_letters_try",None)
    return redirect("pendu")

