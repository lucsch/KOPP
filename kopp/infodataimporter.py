from dataclasses import dataclass
import re

@dataclass
class InfoData:
    title: str = ""
    hr_done_hours: int = 0
    hr_done_minutes: int = 0
    hr_increased_hours: int = 0
    hr_increased_minutes: int = 0
    hr_total_hours: int = 0
    hr_total_minutes: int = 0
    a_hours: int = 0
    a_minutes: int = 0
    piquet_hours: int = 0
    piquet_minutes: int = 0
    vac_hours: int = 0
    vac_minutes: int = 0


class InfoDataImporter:

    HOURS_PER_DAY = 8
    MINUTES_PER_HOUR = 60

    def __init__(self):
        self.m_data = InfoData()

    def process(self, text_to_import : str) -> bool:
        return False

    def _process_line_hours(self, line: str) -> int:
        """ Convert a numeric line into a number. The line may be formatted as follows:
            112h10m : meaning 112 hours and 10 minutes, which will be converted to 112*60 + 10 = 6730 minutes
            13,50j : meaning 13 days and 50% of a day, which will be converted to 13*8*60 + 0.5*8*60 = 6480 minutes
        """
        cleaned_line = line.strip()

        hours_match = re.fullmatch(r"(\d+)h(\d+)m", cleaned_line)
        if hours_match is not None:
            hours = int(hours_match.group(1))
            minutes = int(hours_match.group(2))
            return hours * self.MINUTES_PER_HOUR + minutes

        days_match = re.fullmatch(r"(\d+),(\d+)j", cleaned_line)
        if days_match is not None:
            days = int(days_match.group(1))
            day_fraction = float(f"0.{days_match.group(2)}")
            minutes_per_day = self.HOURS_PER_DAY * self.MINUTES_PER_HOUR
            return round((days + day_fraction) * minutes_per_day)

        return 0


    def get_processed_data(self) -> InfoData:
        return self.m_data
