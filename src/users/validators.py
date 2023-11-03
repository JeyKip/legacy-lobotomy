import re
import string

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(_('The password must contain at least 1 digit, 0-9.'), code='password_no_number')

    def get_help_text(self):
        return _('Your password must contain at least 1 digit, 0-9.')


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.search('[A-Z]', password):
            raise ValidationError(
                _('The password must contain at least 1 uppercase letter, A-Z.'), code='password_no_upper'
            )

    def get_help_text(self):
        return _('Your password must contain at least 1 uppercase later, A-Z.')


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.search('[a-z]', password):
            raise ValidationError(
                _('The password must contain at least 1 lowercase letter, a-z.'), code='password_no_lower'
            )

    def get_help_text(self):
        return _('Your password must contain at least 1 lowercase, a-z.')


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.search(f'[{re.escape(string.punctuation)}]', password):
            raise ValidationError(
                _(f'The password must contain at least 1 symbol: {string.punctuation}'), code='password_no_symbol')

    def get_help_text(self):
        return _(f'Your password must contain at least 1 symbol: {string.punctuation}')


class SpaceValidator(object):
    def validate(self, password, user=None):
        if re.search(r'\s', password):
            raise ValidationError(_('The password must not contain any space character.'), code='password_with_space')

    def get_help_text(self):
        return _('Your password must not contain any space character.')
