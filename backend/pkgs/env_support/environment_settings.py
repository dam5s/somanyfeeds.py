import os
from typing import Optional


class StringSetting:
    @staticmethod
    def optional(name: str) -> Optional[str]:
        return os.environ.get(name)

    @staticmethod
    def with_default(name: str, default: str) -> str:
        return StringSetting.optional(name) or default

    @staticmethod
    def required(name: str) -> str:
        value = os.environ.get(name)
        if value is None:
            raise Exception(f"Environment variable {name} is not set")
        return value

class FloatSetting:
    @staticmethod
    def with_default(name: str, default: float) -> float:
        string_value = StringSetting.optional(name)
        if string_value is None:
            return default
        return float(string_value)
