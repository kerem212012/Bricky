from typing import Any

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import UserLoginForm, UserRegisterForm


def login_view(request) -> Any:
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")

    else:
        form = UserLoginForm()
    return render(request, "user/login.html", context={"form": form})

def registration_view(request) -> Any:
    """
    :param request:
    :return:
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.is_active = True
            user.save()
            send_verification(request, user)
            login(request, user)
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "users/registration.html", context={"form": form})

def user_logout(request) -> Any:
    logout(request)
    return redirect("/")

def send_verification(request, user) -> Any:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("user:verify_email", kwargs={"uidb64": uid, "token": token})
    verify_url = f"http://{domain}{link}"
    subject = "Email confirmation"
    message = render_to_string("users/email_verify.html", {
        "user": user,
        "verify_url": verify_url,
    })

    send_mail(subject, message, None, [user.email])


def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return render(request, "user/email_verified_success.html")
    return render(request, "user/email_verified_failed.html")