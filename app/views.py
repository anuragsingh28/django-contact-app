from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


# def home(request):
#     context = {
#         'contacts': Contact.objects.all()
#     }
#     return render(request, 'index.html', context)


# def detail(request, id):
#     context = {
#         'contact': get_object_or_404(Contact, pk=id)
#     }
#     return render(request, 'detail.html', context)


class HomePageView(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = "index.html"

    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager=self.request.user)


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    context_object_name = 'contact'
    template_name = "detail.html"


@login_required
def search(request):
    if request.GET:
        search_term = request.GET['serach_term']
        serach_result = Contact.objects.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(info__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(name__iexact=search_term)
        )
        context = {
            'search_term': search_term,
            'contacts': serach_result.filter(manager=request.user),
        }
        return render(request, 'search.html', context)
    else:
        return redirect('home')


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = "create.html"
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(
            self.request, 'Your contact has been successfully created')
        return redirect('detail', instance.pk)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = "update.html"
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    success_url = '/'

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'Your contact has been successfully Updated')
        return redirect('detail', instance.pk)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "delete.html"
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Your contact has been successfully deleted')
        return super().delete(self, request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
