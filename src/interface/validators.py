from enum import Enum

from ..backend.backend_helpers import BackendHelpers
from ..backend.errors import InterfaceError


class ValidatorTypes(Enum):
    ONE_WORD_NO_NUMBERS_OR_SPECIAL_CHARACTERS = "One Word, No Numbers or Special Characters"
    JUST_A_Z = "Just a-z not spaces."
    SENTENCE_NO_NUMBERS_OR_SPECIAL_CHARACTERS = "Sentence with Numbers or Special Characters"
    NUMBERS_ONLY = "Numbers Only"


class UIValidators(BackendHelpers):
    def __init__(self, root):
        self.validators = {
            ValidatorTypes.ONE_WORD_NO_NUMBERS_OR_SPECIAL_CHARACTERS: root.register(self.re_word_without_spaces),
            ValidatorTypes.SENTENCE_NO_NUMBERS_OR_SPECIAL_CHARACTERS: root.register(self.re_word_with_spaces),
            ValidatorTypes.JUST_A_Z: root.register(self.re_word_a_z),
            ValidatorTypes.NUMBERS_ONLY: root.register(self.re_numbers_only)
        }

    def validate_field(self, field, validator):
        field.config(
            validate="key",
            validatecommand=(self.validators[validator], '%P')
        )

    @staticmethod
    def bulk_check(fields):
        for fi in fields.items():
            if len(fi[1].get()) == 0:
                raise InterfaceError(f"{fi[0].title()} is empty.")
