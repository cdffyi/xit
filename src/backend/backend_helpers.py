import re


class BackendHelpers:
    @staticmethod
    def re_word_without_spaces(string_to_match):
        if re.match("^[a-zA-Z]+$", string_to_match):
            return True
        elif string_to_match == "":
            return True
        return False

    @staticmethod
    def re_word_with_spaces(string_to_match):
        if re.match("^([a-zA-Z.]+\\s?)+$", string_to_match):
            return True
        elif string_to_match == "":
            return True
        return False

    @staticmethod
    def re_word_a_z(string_to_match):
        if re.match("^[a-z]+$", string_to_match):
            return True
        elif string_to_match == "":
            return True
        return False

    @staticmethod
    def re_numbers_only(string_to_match):
        if re.match("^\\d+$", string_to_match):
            return True
        elif string_to_match == "":
            return True
        return False
