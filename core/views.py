from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, View, CreateView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
import json

from .models import ContactMessage, NewsletterSubscription
from .forms import ContactForm, NewsletterSubscriptionForm



# ============ LEGAL & INFO PAGES ============
class PrivacyPolicyView(TemplateView):
    """
    View for displaying the Privacy Policy page
    """
    template_name = 'core/legal/privacy.html'


class TermsOfServiceView(TemplateView):
    """
    View for displaying the Terms of Service page
    """
    template_name = 'core/legal/terms.html'


class AboutView(TemplateView):
    """
    View for displaying the About page
    """
    template_name = 'core/pages/about.html'


class ContactView(TemplateView):
    """
    View for displaying and handling the Contact page form
    """
    template_name = 'core/pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['subject_choices'] = ContactMessage.SubjectChoice.choices
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle form submission"""
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




# ============ NEWSLETTER VIEWS ============
class NewsletterSubscribeView(CreateView):
    """
    View for subscribing to the newsletter
    """
    model = NewsletterSubscription
    form_class = NewsletterSubscriptionForm
    template_name = 'notifications/subscribe/newsletter_subscribe.html'
    success_url = reverse_lazy('core:newsletter_success')

    def form_valid(self, form):
        """Handle successful form submission"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Thank you for subscribing to our newsletter! You\'ll receive updates soon.'
        )
        return response

    def form_invalid(self, form):
        """Handle form errors"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return self.render_to_response(self.get_context_data(form=form))


class NewsletterSubscribeAjaxView(View):
    """
    AJAX view for subscribing to the newsletter
    """
    def post(self, request):
        """Handle AJAX POST request"""
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()

            if not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Email is required.'
                }, status=400)

            # Check if already subscribed
            if NewsletterSubscription.objects.filter(email=email, status='active').exists():
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter.'
                }, status=400)

            # Create subscription
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={'status': 'active'}
            )

            if not created and subscription.status == 'unsubscribed':
                # Reactivate unsubscribed email
                subscription.status = 'active'
                subscription.unsubscribed_at = None
                subscription.save()

            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter!'
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }, status=500)


class NewsletterSuccessView(TemplateView):
    """
    Success page after newsletter subscription
    """
    template_name = 'core/newsletter/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Newsletter Subscription Successful'
        return context
