from django.db import models

RACE_TYPE_AMATEUR = 0
RACE_TYPE_OPEN = 1
RACE_TYPE_MASTERS = 2

RACE_TYPES_LITERALS = {
    RACE_TYPE_AMATEUR: 'amateur',
    RACE_TYPE_OPEN: 'open',
    RACE_TYPE_MASTERS: 'master',
}

RACE_TYPES = (
    (RACE_TYPE_AMATEUR, 'Amateur'),
    (RACE_TYPE_OPEN, 'Open'),
    (RACE_TYPE_MASTERS, 'Master'),
)


class Race(models.Model):
    name = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RaceContestant(models.Model):
    race = models.ForeignKey(Race, related_name='contestants', on_delete=models.CASCADE)
    name = models.TextField()
    helmet_number = models.IntegerField(null=True, blank=True)
    qualification_number = models.IntegerField(null=True, blank=True)
    is_amateur = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.helmet_number}: {self.name}'

    @property
    def best_qualification_time(self):
        best_qualification = self.qualifications.all().order_by('qualification_time_ms').first()
        if not best_qualification:
            return None
        return best_qualification.qualification_time_ms / 1000


class RaceContestantQualification(models.Model):
    contestant = models.ForeignKey(RaceContestant, related_name='qualifications', on_delete=models.CASCADE)
    qualification_time_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.contestant.name}: {self.qualification_time}'

    @property
    def qualification_time(self):
        return self.qualification_time_ms / 1000

    @property
    def contestant_name(self):
        return self.contestant.name

    @property
    def race(self):
        return self.contestant.race


class RaceBracket(models.Model):
    race = models.ForeignKey(Race, related_name='brackets', on_delete=models.CASCADE)
    next_bracket = models.ForeignKey('self', null=True, related_name='parent_brackets', on_delete=models.SET_NULL)
    type = models.SmallIntegerField(choices=RACE_TYPES, db_index=True)
    level = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID {self.id}: {self.level} level, bracket of {self.race.name} (type: {self.get_type_display()})'

    def set_level(self):
        level = 0
        parent_bracket = self.parent_brackets.all().first()
        if parent_bracket:
            level = parent_bracket.level + 1
        self.level = level
        self.save()


class BracketContestant(models.Model):
    contestant = models.ForeignKey(RaceContestant, related_name='brackets', on_delete=models.CASCADE)
    bracket = models.ForeignKey(RaceBracket, related_name='contestants', on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Bracket {self.bracket_id} ({self.bracket.level} level): {self.contestant.name}: {self.position}'

    @property
    def bracket_level(self):
        return self.bracket.level

    @property
    def contestant_name(self):
        return self.contestant.name

    @property
    def qualification_number(self):
        return self.contestant.qualification_number

    @property
    def helmet_number(self):
        return self.contestant.helmet_number
