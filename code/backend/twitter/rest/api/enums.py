from enum import Enum, unique


@unique
class Policy(Enum):
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    KEYWORDS = "keywords"
    USERNAME = "username"

    def describe(self):
        return self.name, self.value

    @classmethod
    def api_types(cls):
        return [cls.describe(cls.INSTAGRAM), cls.describe(cls.TWITTER)]

    @classmethod
    def api_filter(cls):
        return [cls.describe(cls.KEYWORDS), cls.describe(cls.USERNAME)]
