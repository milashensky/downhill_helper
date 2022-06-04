from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from races.models import RACE_TYPES, RACE_TYPE_OPEN


class CreateInitialBracketsForm(forms.Form):
    type = forms.ChoiceField(choices=RACE_TYPES, initial=RACE_TYPE_OPEN)
    contestants_per_bracket = forms.IntegerField(initial=4, validators=(MinValueValidator(1), MaxValueValidator(100)))


class CreateStageBracketsForm(CreateInitialBracketsForm):
    num_winner_contestants = forms.IntegerField(initial=2, validators=(MinValueValidator(1), MaxValueValidator(100)))
