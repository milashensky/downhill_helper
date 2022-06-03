import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class CommonTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return ''.join([
            six.text_type(user.pk),
            user.password,
            six.text_type(timestamp)
        ])


token_generator = CommonTokenGenerator()
