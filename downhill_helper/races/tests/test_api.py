from django.urls import reverse
from django.test import TestCase

from races.models import (
    Race, RaceContestant, RaceContestantQualification, BracketContestant,
    RaceBracket, RACE_TYPE_OPEN, RACE_TYPE_AMATEUR)


class ApiTests(TestCase):

    def test_race_api(self):
        race = Race.objects.create(name='speedy', slug='speedy')
        url = reverse('races:race_api', kwargs={'race_slug': race.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'name': race.name,
            'background_image_url': race.background_image_url,
            'is_qualification_open': race.is_qualification_open,
            'has_masters': race.has_masters,
            'has_open': race.has_open,
            'has_amateurs': race.has_amateurs,
        })

    def test_qualification_api(self):
        race = Race.objects.create(name='speedy', slug='speedy')
        contestant1 = RaceContestant.objects.create(race=race, name='shrek')
        contestant2 = RaceContestant.objects.create(race=race, name='megamind')

        qualis = [
            RaceContestantQualification.objects.create(contestant=contestant1, qualification_time_ms=40000),
            RaceContestantQualification.objects.create(contestant=contestant1, qualification_time_ms=41000),
            RaceContestantQualification.objects.create(contestant=contestant2, qualification_time_ms=42000),
            RaceContestantQualification.objects.create(contestant=contestant2, qualification_time_ms=43000),
        ]

        url = reverse('races:qualification_api', kwargs={'race_slug': race.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': contestant_quali.id,
            'contestant_name': contestant_quali.contestant_name,
            'qualification_time': contestant_quali.qualification_time,
            'helmet_number': contestant_quali.helmet_number,
        } for contestant_quali in qualis])

    def test_brackets_api(self):
        race = Race.objects.create(name='speedy', slug='speedy')
        bracket2 = RaceBracket.objects.create(race=race, type=RACE_TYPE_OPEN)
        bracket1 = RaceBracket.objects.create(race=race, next_bracket=bracket2, type=RACE_TYPE_OPEN)
        bracket2_amateur = RaceBracket.objects.create(race=race, type=RACE_TYPE_AMATEUR)
        bracket1_amateur = RaceBracket.objects.create(race=race, next_bracket=bracket2_amateur, type=RACE_TYPE_AMATEUR)
        contestant1 = RaceContestant.objects.create(race=race, name='shrek', is_amateur=True)
        contestant2 = RaceContestant.objects.create(race=race, name='megamind', is_amateur=True)

        brackets = [
            BracketContestant.objects.create(bracket=bracket1, contestant=contestant1, position=1),
            BracketContestant.objects.create(bracket=bracket2, contestant=contestant1),
            BracketContestant.objects.create(bracket=bracket1, contestant=contestant2, position=2),
            BracketContestant.objects.create(bracket=bracket2, contestant=contestant2),
        ]
        brackets_amateur = [
            BracketContestant.objects.create(bracket=bracket1_amateur, contestant=contestant1, position=2),
            BracketContestant.objects.create(bracket=bracket2_amateur, contestant=contestant1),
            BracketContestant.objects.create(bracket=bracket1_amateur, contestant=contestant2, position=1),
            BracketContestant.objects.create(bracket=bracket2_amateur, contestant=contestant2),
        ]

        url = reverse('races:brackets_api', kwargs={'race_slug': race.slug, 'type': RACE_TYPE_OPEN})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': bracket_contestant.id,
            'contestant_name': bracket_contestant.contestant_name,
            'helmet_number': bracket_contestant.helmet_number,
            'qualification_number': bracket_contestant.qualification_number,
            'position': bracket_contestant.position,
            'bracket_id': bracket_contestant.bracket_id,
            'bracket_level': bracket_contestant.bracket_level,
        } for bracket_contestant in brackets])
        url = reverse('races:brackets_api', kwargs={'race_slug': race.slug, 'type': RACE_TYPE_AMATEUR})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': bracket_contestant.id,
            'contestant_name': bracket_contestant.contestant_name,
            'helmet_number': bracket_contestant.helmet_number,
            'qualification_number': bracket_contestant.qualification_number,
            'position': bracket_contestant.position,
            'bracket_id': bracket_contestant.bracket_id,
            'bracket_level': bracket_contestant.bracket_level,
        } for bracket_contestant in brackets_amateur])
