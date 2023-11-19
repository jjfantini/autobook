from typing import Optional, Union


class RangeFormatError(BaseException):
    """Range Retrieval Error."""

    def __init__(self, original: Optional[Union[str, Exception]] = None):
        self.original = original
        super().__init__(str(original))


class WrongArgumentsError(BaseException):
    """Wrong Arguments Error."""

    def __init__(self, original: Optional[Union[str, Exception]] = None):
        self.original = original
        super().__init__(str(original))


class HumblDataError(BaseException):
    """Wrong Arguments Error."""

    def __init__(self, original: Optional[Union[str, Exception]] = None):
        self.original = original
        super().__init__(str(original))
