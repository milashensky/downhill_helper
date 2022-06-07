import math
from sensors.models import SensorSignal, START_SENSOR_MARK, FINISH_SENSOR_MARK
from races.models import RACE_TYPE_OPEN, RACE_TYPES_LITERALS, RaceBracket, BracketContestant, RaceContestantQualification


def create_initial_brackets(race, type=RACE_TYPE_OPEN, contestants_per_bracket=4):
    """Creates an initial brackets after quali, distributing quali leading contestants
    into different brackets (packs)
    """
    type_literal = RACE_TYPES_LITERALS.get(int(type))
    type_filter = {
        f'is_{type_literal}': True,
    }
    contestants = race.contestants.filter(**type_filter).order_by('qualification_number')
    # check the quali is over
    if contestants.filter(qualification_number=None).exists():
        return
    # if in last bracket will be less contestants then 1/2 of required -> last bracket will be flooded
    # else, one more braket will be created.
    # but at least one should be created
    brackets_number = round(contestants.count() / contestants_per_bracket) or 1
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


def create_stage_brackets(race, type=RACE_TYPE_OPEN, contestants_per_bracket=4, num_winner_contestants=2):
    """Creates a next set of brackets from last finished brackets.
    New brackets will contain `contestants_per_bracket` contestants,
    `num_winner_contestants` leading contestants will be taken from previous level bracket.
    """
    # higher level goes first, to take the highest level
    brackets = race.brackets.filter(type=type).order_by('-level')
    if not brackets:
        return
    # filtering out lower levels
    bracket_level = brackets.first().level
    last_brackets = brackets.filter(level=bracket_level)
    contestants = BracketContestant.objects.filter(bracket__in=last_brackets, position__lte=num_winner_contestants).order_by('bracket_id')
    # if some bracket is not finished yet, return
    if not contestants.count():
        return
    next_bracket = RaceBracket.objects.create(race=race, type=type)
    for contestant in contestants:
        if next_bracket.contestants.count() == contestants_per_bracket:
            next_bracket.set_level()
            next_bracket = RaceBracket.objects.create(race=race, type=int(type))
        contestant.bracket.next_bracket = next_bracket
        contestant.bracket.save()
        new_contestant = BracketContestant.objects.create(contestant=contestant.contestant, bracket=next_bracket)
    next_bracket.set_level()


def set_qualification_time_by_sensors_data(contestant):
    """assigns the qualification time to the contestant based on a last sensors data
    """
    start_filters = {
        'contestant__isnull': True,
        'sensor_mark': START_SENSOR_MARK,
    }
    last_signed_time = SensorSignal.objects.filter(contestant__isnull=False).order_by('signal_registered_at').last()
    if last_signed_time:
        start_filters['signal_registered_at__gt'] = last_signed_time.signal_registered_at
    start_signal = SensorSignal.objects.filter(**start_filters).order_by('signal_registered_at').last()
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
    return contestant_qualification


def set_qualification_numbers(race):
    """assings qualification numbers to the contestants based on their quali times
    """
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
