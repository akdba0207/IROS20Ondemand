# * Copyright (C) Dongbin Kim - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Dongbin Kim <akdba0207@gmail.com>, September, 2020
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
           six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()