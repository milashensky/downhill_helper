from django.test import TestCase
from sensors.models import SensorSignal, START_SENSOR_MARK, FINISH_SENSOR_MARK
from races.models import Race, RaceContestant, RaceBracket
from races.utils import set_qualification_time_by_sensors_data, set_qualification_numbers, create_initial_brackets, create_stage_brackets


class UtilsTests(TestCase):

    def test_set_qualification_time_by_sensors_data(self):
        race = Race.objects.create(name='speedy')
        contestant1 = RaceContestant.objects.create(race=race, name='shrek')
        contestant2 = RaceContestant.objects.create(race=race, name='megamind')
        set_qualification_time_by_sensors_data(contestant1)
        self.assertEqual(contestant1.best_qualification_time, None)
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:00:00')
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:00:01')
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:00:02')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:00')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:01')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:02')
        # should take last free start signal time,
        # and last end signal after a start time
        set_qualification_time_by_sensors_data(contestant1)
        self.assertEqual(contestant1.best_qualification_time, 60.0)

        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:03')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:50')
        set_qualification_time_by_sensors_data(contestant2)
        self.assertEqual(contestant2.best_qualification_time, 47.0)
        # nothing has been changed, the signal has been taken
        set_qualification_time_by_sensors_data(contestant1)
        self.assertEqual(contestant1.best_qualification_time, 60.0)
        self.assertEqual(contestant1.qualifications.count(), 1)

        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:51')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:02:35')
        set_qualification_time_by_sensors_data(contestant1)
        self.assertEqual(contestant1.best_qualification_time, 44.0)
        self.assertEqual(contestant1.qualifications.count(), 2)

    def test_set_qualification_numbers(self):
        race = Race.objects.create(name='speedy')
        contestant1 = RaceContestant.objects.create(race=race, name='shrek')
        contestant2 = RaceContestant.objects.create(race=race, name='megamind')
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:00:00')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:01:00')
        set_qualification_time_by_sensors_data(contestant1)
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:02:00')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:02:30')
        set_qualification_time_by_sensors_data(contestant1)
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:03:00')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:03:40')
        set_qualification_time_by_sensors_data(contestant2)
        SensorSignal.objects.create(race=race, sensor_mark=START_SENSOR_MARK, signal_registered_at='2020-01-02 00:04:00')
        SensorSignal.objects.create(race=race, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at='2020-01-02 00:04:50')
        set_qualification_time_by_sensors_data(contestant2)
        set_qualification_numbers(race)
        contestant1.refresh_from_db()
        contestant2.refresh_from_db()
        self.assertEqual(contestant1.qualification_number, 1)
        self.assertEqual(contestant2.qualification_number, 2)
        self.assertTrue(contestant1.best_qualification_time < contestant2.best_qualification_time)

    def test_create_initial_brackets(self):
        race = Race.objects.create(name='speedy')
        contestant1 = RaceContestant.objects.create(race=race, name='some', qualification_number=1)
        contestant2 = RaceContestant.objects.create(race=race, name='body', qualification_number=2)
        contestant3 = RaceContestant.objects.create(race=race, name='once', qualification_number=3)
        contestant4 = RaceContestant.objects.create(race=race, name='told', qualification_number=4)
        contestant5 = RaceContestant.objects.create(race=race, name='me', qualification_number=5)
        contestant6 = RaceContestant.objects.create(race=race, name='the', qualification_number=6)
        contestant7 = RaceContestant.objects.create(race=race, name='world', qualification_number=7)
        contestant8 = RaceContestant.objects.create(race=race, name='is', qualification_number=8)
        contestant9 = RaceContestant.objects.create(race=race, name='gonna', qualification_number=9)
        contestant10 = RaceContestant.objects.create(race=race, name='roll', qualification_number=10)
        contestant11 = RaceContestant.objects.create(race=race, name='me', qualification_number=11)
        create_initial_brackets(race)
        brackets = RaceBracket.objects.filter(race=race)
        self.assertEqual(brackets.count(), 3)
        self.assertEqual(brackets[0].contestants.count(), 4)
        self.assertEqual(brackets[1].contestants.count(), 4)
        self.assertEqual(brackets[2].contestants.count(), 3)
        first_contestants_ids = brackets[0].contestants.values_list('contestant_id', flat=True)
        self.assertTrue(contestant1.id in first_contestants_ids)
        self.assertTrue(contestant4.id in first_contestants_ids)
        self.assertTrue(contestant7.id in first_contestants_ids)
        self.assertTrue(contestant10.id in first_contestants_ids)
        create_initial_brackets(race, contestants_per_bracket=40)
        # all brackets are cleared up and one created instead
        self.assertEqual(brackets.count(), 1)

    def test_create_stage_brackets(self):
        race = Race.objects.create(name='speedy')
        contestant1 = RaceContestant.objects.create(race=race, name='some', qualification_number=1)
        contestant2 = RaceContestant.objects.create(race=race, name='body', qualification_number=2)
        contestant3 = RaceContestant.objects.create(race=race, name='once', qualification_number=3)
        contestant4 = RaceContestant.objects.create(race=race, name='told', qualification_number=4)
        contestant5 = RaceContestant.objects.create(race=race, name='me', qualification_number=5)
        contestant6 = RaceContestant.objects.create(race=race, name='the', qualification_number=6)
        contestant7 = RaceContestant.objects.create(race=race, name='world', qualification_number=7)
        contestant8 = RaceContestant.objects.create(race=race, name='is', qualification_number=8)
        create_initial_brackets(race)
        brackets = RaceBracket.objects.filter(race=race)
        self.assertEqual(brackets.count(), 2)
        create_stage_brackets(race)
        brackets = RaceBracket.objects.filter(race=race)
        # no new brackets, since previous brackets aren't closed
        self.assertEqual(brackets.count(), 2)
        for bracket in brackets:
            self.assertEqual(bracket.level, 0)
            # settings positions
            for i, contestant in enumerate(bracket.contestants.all().order_by('contestant__qualification_number')):
                contestant.position = i + 1
                contestant.save()

        create_stage_brackets(race)
        new_brackets = RaceBracket.objects.filter(race=race).exclude(level=0)
        self.assertEqual(new_brackets.count(), 1)
        new_bracket = new_brackets.first()
        for bracket in brackets:
            bracket.refresh_from_db()
            self.assertEqual(bracket.next_bracket, new_bracket)
        self.assertEqual(new_bracket.level, 1)
        contestants_ids = new_bracket.contestants.values_list('contestant_id', flat=True)
        self.assertTrue(contestant1.id in contestants_ids)
        self.assertTrue(contestant2.id in contestants_ids)
        self.assertTrue(contestant3.id in contestants_ids)
        self.assertTrue(contestant4.id in contestants_ids)
