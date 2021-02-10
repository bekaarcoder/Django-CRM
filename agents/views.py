import random
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
  template_name = 'agents/agent_list.html'

  def get_queryset(self):
    organisation = self.request.user.userprofile
    return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
  template_name = 'agents/agent_create.html'
  form_class = AgentModelForm

  def get_success_url(self):
    return reverse('agents:agent-list')

  def form_valid(self, form):
    user = form.save(commit=False)
    user.is_agent = True
    user.is_organizer = False

    default_password = f"{random.randint(0, 1000000)}"
    user.set_password(default_password)

    user.save()
    Agent.objects.create(
      user=user,
      organisation=self.request.user.userprofile
    )
    # send email to agent
    send_mail(
      subject="Agent Created For DJCRM",
      message=f"You have been invited as an agent on DJCRM. Please login to you account to start working. Your default password is {default_password}",
      from_email='admin@admin.com',
      recipient_list=[user.email]
    )
    return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
  template_name = 'agents/agent_detail.html'
  context_object_name = 'agent'

  def get_queryset(self):
    organisation = self.request.user.userprofile
    return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
  template_name = 'agents/agent_update.html'
  form_class = AgentModelForm

  def get_queryset(self):
    organisation = self.request.user.userprofile
    return Agent.objects.filter(organisation=organisation)

  def get_success_url(self):
    return reverse('agents:agent-list')


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
  template_name = 'agents/agent_delete.html'

  def get_queryset(self):
    organisation = self.request.user.userprofile
    return Agent.objects.filter(organisation=organisation)

  def get_success_url(self):
    return reverse('agents:agent-list')