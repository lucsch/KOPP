class TimeConverter:
    """Convert hours/minutes pairs to total minutes and back."""

    @staticmethod
    def to_total_minutes(hours: int, minutes: int) -> int:
        if not isinstance(hours, int) or not isinstance(minutes, int):
            raise TypeError("hours and minutes must be integers")
        if minutes <= -60 or minutes >= 60:
            raise ValueError("minutes must be between -59 and 59")

        return hours * 60 + minutes

    @staticmethod
    def from_total_minutes(total_minutes: int) -> tuple[int, int]:
        if not isinstance(total_minutes, int):
            raise TypeError("total_minutes must be an integer")

        sign = -1 if total_minutes < 0 else 1
        hours, minutes = divmod(abs(total_minutes), 60)
        return sign * hours, sign * minutes
