class TimeConverter:
    """Convert hours/minutes pairs to total minutes and back."""

    @staticmethod
    def to_total_minutes(hours: int, minutes: int) -> int:
        if not isinstance(hours, int) or not isinstance(minutes, int):
            raise TypeError("hours and minutes must be integers")
        if hours < 0:
            raise ValueError("hours must be greater than or equal to 0")
        if minutes < 0 or minutes >= 60:
            raise ValueError("minutes must be between 0 and 59")

        return hours * 60 + minutes

    @staticmethod
    def from_total_minutes(total_minutes: int) -> tuple[int, int]:
        if not isinstance(total_minutes, int):
            raise TypeError("total_minutes must be an integer")
        if total_minutes < 0:
            raise ValueError("total_minutes must be greater than or equal to 0")

        return divmod(total_minutes, 60)
