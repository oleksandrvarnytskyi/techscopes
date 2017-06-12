from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import User
from .forms import SignUpForm
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.city = form.cleaned_data.get('city')
            user.save()
            # Send the account activation email for the user
            current_site = get_current_site(request)
            subject = 'Activate Your Techscopes Account'
            message = render_to_string(
                'accounts/account_activation_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    """Check if the user exists, if the token is valid. Switch the flags
    is_active and email_confirmed to True and log the user in. By changing the
    value of the email_confirmed field, it will cause the link to be
    invalidated."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('main')
    else:
        return render(request, 'accounts/account_activation_invalid.html')
