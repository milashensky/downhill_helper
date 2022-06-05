from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required

from races import utils as race_utils
from races.models import Race
from races.forms import CreateInitialBracketsForm, CreateStageBracketsForm


class RaceActionMixin:

    @classmethod
    def as_view(cls, *args, **kwargs):
        return staff_member_required(super().as_view(*args, **kwargs))

    def get_race(self):
        return get_object_or_404(Race, id=self.kwargs.get('race_id'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['race'] = self.get_race()
        return context

    def get_success_url(self):
        return reverse('admin:races_race_changelist')


class CreateInitialBracketsView(RaceActionMixin, FormView):
    template_name = 'admin/races/create_initial_brackets.html'
    form_class = CreateInitialBracketsForm

    def form_valid(self, form):
        race = self.get_race()
        race_utils.set_qualification_numbers(race)
        race_utils.create_initial_brackets(race, **form.cleaned_data)
        return super().form_valid(form)


class CreateStageBracketsView(RaceActionMixin, FormView):
    template_name = 'admin/races/create_stage_brackets.html'
    form_class = CreateStageBracketsForm

    def form_valid(self, form):
        race = self.get_race()
        race_utils.create_stage_brackets(race, **form.cleaned_data)
        return super().form_valid(form)
