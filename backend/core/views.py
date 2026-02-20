from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages

from .models import ContactMessage
from .forms import ContactForm

# ===== Content Pages =====

class AboutView(TemplateView):
    template_name = 'core/pages/about.html'

# ===== Legal Pages =====

class PrivacyPolicyView(TemplateView):
    template_name = 'core/legal/privacy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'core/legal/terms.html'

# ===== Contact Page =====

class ContactView(TemplateView):
    template_name = 'core/pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['subject_choices'] = ContactMessage.SubjectChoice.choices
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Save the contact message
            contact_message = form.save()
            
            messages.success(
                request,
                f'Thank you for your message! We will get back to you at {contact_message.email} within 24 business hours.'
            )
            
            # Redirect to same page to clear form
            return redirect('core:contact')
        else:
            # Return with form errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

