import logging

from django.shortcuts import get_object_or_404

from common.mixins import SerializedView, CsrfExemptMixin
from races.models import Race, BracketContestant, RaceContestantQualification

logger = logging.getLogger(__name__)


class RaceApi(CsrfExemptMixin, SerializedView):
    fields = ('name', 'background_image_url', 'is_qualification_open', 'has_masters', 'has_open', 'has_amateurs')

    def get(self, request, race_slug):
        return get_object_or_404(Race, slug=race_slug)


class QualificationApi(CsrfExemptMixin, SerializedView):
    fields = ('id', 'contestant_name', 'qualification_time', 'helmet_number')

    def get(self, request, race_slug):
        race = get_object_or_404(Race, slug=race_slug)
        return RaceContestantQualification.objects.filter(contestant__race=race).prefetch_related('contestant')


class BracketsApi(CsrfExemptMixin, SerializedView):
    fields = ('id', 'contestant_name', 'helmet_number', 'qualification_number', 'position', 'bracket_id', 'bracket_level')

    def get(self, request, race_slug, type):
        race = get_object_or_404(Race, slug=race_slug)
        return BracketContestant.objects.filter(bracket__type=type, contestant__race=race).prefetch_related('contestant', 'bracket')
