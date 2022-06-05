from urllib.parse import urlencode
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from races.models import Race, RACE_TYPE_OPEN


class ViewsTests(TestCase):

    def setUp(self):
        self.race = Race.objects.create(name='speedy')
        self.user = User.objects.create_user(username='imposter', email='this_is_kinda_sus@gmail.com', password='somebody_once_told_me', is_staff=False)
        self.staff_user = User.objects.create_user(username='shrek', email='this_is_my_swamp@gmail.com', password='somebody_once_told_me', is_staff=True)

    def test_create_initial_brackets_view(self):
        url = reverse('admin:create_initial_brackets_view', kwargs={'race_id': self.race.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # get with non staff user
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # get with staff user
        self.client.force_login(user=self.staff_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # post form
        data = {
            'type': str(RACE_TYPE_OPEN),
            'contestants_per_bracket': 4,
        }
        with patch('races.utils.create_initial_brackets') as create_initial_brackets_mock, patch('races.utils.set_qualification_numbers') as set_qualification_numbers_mock:
            response = self.client.post(url, urlencode(data), content_type='application/x-www-form-urlencoded')
            set_qualification_numbers_mock.assert_called_with(self.race)
            create_initial_brackets_mock.assert_called_with(self.race, **data)
            # redirect to races
            self.assertEqual(response.status_code, 302)

        # no existing race
        url = reverse('admin:create_initial_brackets_view', kwargs={'race_id': self.race.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_stage_brackets_view(self):
        url = reverse('admin:create_stage_brackets_view', kwargs={'race_id': self.race.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # get with non staff user
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # get with staff user
        self.client.force_login(user=self.staff_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # post form
        data = {
            'type': str(RACE_TYPE_OPEN),
            'contestants_per_bracket': 4,
            'num_winner_contestants': 2,
        }
        with patch('races.utils.create_stage_brackets') as create_stage_brackets_mock:
            response = self.client.post(url, urlencode(data), content_type='application/x-www-form-urlencoded')
            create_stage_brackets_mock.assert_called_with(self.race, **data)
            # redirect to races
            self.assertEqual(response.status_code, 302)

        # no existing race
        url = reverse('admin:create_stage_brackets_view', kwargs={'race_id': self.race.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
