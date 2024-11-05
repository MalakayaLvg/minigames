from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

import spacy
from website.forms import PenduForm, CemantixForm


# Create your views here.

def index(request):
    return render(request,"website/home.html")

def pendu_start(request):

    request.session['user_letters_guessed'] = 0
    request.session['user_letters_try'] = []
    request.session['user_all_try'] = []



def pendu(request):
    guess_word = "carambar"
    guess_word_length = len(guess_word)
    guess_word_letters = list(guess_word)
    user_letters_guessed = request.session.get("user_letters_guessed",0)
    user_letters_try = request.session.get("user_letters_try",[])
    user_all_try = request.session.get("user_all_try",[])

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
                user_all_try.append(user_letter)
                request.session["user_all_try"] = user_all_try
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
                       "user_letters_guessed": user_letters_guessed,"user_letters_try":user_letters_try,"user_all_try":user_all_try,
                       "guess_word_length":guess_word_length}
            return render(request, "pendu/index.html", context)


    else:
        form = PenduForm()

    context = {"form": form}
    return render(request,"pendu/index.html", context)

def pendu_reset(request):
    request.session.pop("user_letters_guessed",None)
    request.session.pop("user_letters_try",None)
    return redirect("pendu")

def cemantix_start(request):
    request.session["user_list"] = []

def cemantix(request):
    llm = spacy.load("en_core_web_lg")
    secret_word = "concrete"
    token_secret_word = llm(secret_word)
    user_list = request.session.get("user_list",[])

    if request.method == "POST":
        form = CemantixForm(request.POST)
        if form.is_valid():
            user_word = form.cleaned_data["word"]
            token_user_word = llm(user_word)

            if secret_word == user_word:
                similarity = 1
            else:
                similarity =token_user_word.similarity(token_secret_word)

            if similarity == 1:
                state = "you won !"
            else:
                state = "try again !"


            similarity = round(similarity,2)*100
            word_info = {"user_word":user_word,"similarity":similarity}
            user_list.append(word_info)
            request.session["user_list"] = user_list

            context = {"form": form, "user_word":user_word, "state":state, "similarity":similarity, "user_list":user_list}
            return render(request, "cemantix/index.html", context)

    form = CemantixForm
    context = {"form":form}
    return render(request, "cemantix/index.html",context)

def cemantix_reset(request):

    request.session.pop("user_list",None)
    return redirect("cemantix")

