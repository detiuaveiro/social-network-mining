from enum import Enum, unique


@unique
class Policy(Enum):
    INSTAGRAM = "Instagram"
    TWITTER = "Twitter"
    KEYWORDS = "Keywords"
    TARGET = "Target"

    def describe(self):
        return self.value, self.name

    @classmethod
    def api_types(cls):
        return [cls.describe(cls.INSTAGRAM), cls.describe(cls.TWITTER)]

    @classmethod
    def api_filter(cls):
        return [cls.describe(cls.KEYWORDS), cls.describe(cls.TARGET)]
