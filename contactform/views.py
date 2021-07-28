from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContactForm


# def contactForm(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = "Website Inquiry"
#             body = {
#                 'first_name': form.cleaned_data['first_name'],
#                 'last_name': form.cleaned_data['last_name'],
#                 'email': form.cleaned_data['email_address'],
#                 'message': form.cleaned_data['message'],
#             }
#             message = "\n".join(body.values())

#             try:
#                 send_mail(subject, message, 'admin@example.com',
#                           ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect("home")

#     form = ContactForm()
#     return render(request, "contactform/contactus.html", {'form': form})


def contactForm(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email_subject = f'New contact {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
            return render(request, 'contactform/success.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'contactform/contactus.html', context)
