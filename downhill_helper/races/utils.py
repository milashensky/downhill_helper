from sensors.models import SensorSignal, START_SENSOR_MARK, FINISH_SENSOR_MARK
from races.models import RACE_TYPE_OPEN, RaceBracket, BracketContestant, RaceContestantQualification


def create_initial_brackets(race, type=RACE_TYPE_OPEN, contestants_per_bracket=4):
    contestants = race.contestants.all().order_by('qualification_number')
    # if in last bracket will be less contestants then 1/2 of required -> last bracket will be flooded
    # else, one more braket will be created.
    brackets_number = round(contestants.count() / contestants_per_bracket)
    # removing all previous brackets
    RaceBracket.objects.all().delete()
    brackets = RaceBracket.objects.bulk_create([RaceBracket(race=race, type=type) for _ in range(0, brackets_number)])
    # first goes in the 1st bracket, 2nd in the seconds, etc, cycled
    add_to_bracket = 0
    for contestant in contestants:
        BracketContestant.objects.create(
            contestant=contestant,
            bracket=brackets[add_to_bracket],
        )
        add_to_bracket += 1
        if add_to_bracket >= brackets_number:
            add_to_bracket = 0


def create_stage_brackets():
    pass


def set_qualification_time_by_sensors_data(contestant):
    start_filters = {
        'contestant__isnull': True,
        'sensor_mark': START_SENSOR_MARK,
    }
    last_signed_time = SensorSignal.objects.filter(contestant__isnull=False).order_by('signal_registered_at').last()
    if last_signed_time:
        start_filters['signal_registered_at__gt'] = last_signed_time.signal_registered_at
    start_signal = SensorSignal.objects.filter(**start_filters).order_by('signal_registered_at').first()
    if not start_signal:
        return

    end_signal = SensorSignal.objects.filter(
        contestant__isnull=True, sensor_mark=FINISH_SENSOR_MARK, signal_registered_at__gt=start_signal.signal_registered_at
    ).order_by('signal_registered_at').last()
    if not end_signal:
        return
    diff = end_signal.signal_registered_at - start_signal.signal_registered_at
    qualification_time_ms = int(diff.total_seconds() * 1000)
    contestant_qualification = RaceContestantQualification.objects.create(
        contestant=contestant, qualification_time_ms=qualification_time_ms)
    start_signal.contestant = contestant_qualification
    start_signal.save()
    end_signal.contestant = contestant_qualification
    end_signal.save()


def set_qualification_numbers(race):
    qualifications = RaceContestantQualification.objects.filter(contestant__race=race).order_by('qualification_time_ms')
    i = 1
    contestants = set()
    for qualification in qualifications:
        if qualification.contestant in contestants:
            continue
        qualification.contestant.qualification_number = i
        qualification.contestant.save()
        contestants.add(qualification.contestant)
        i += 1
