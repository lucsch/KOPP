from dataclasses import dataclass
from enum import Enum, auto
import re
from kopp.timeconverter import TimeConverter


class InfoLineType(Enum):
    ANNUALISATION = auto()
    SOLDE_VACANCES = auto()
    SOLDE_HS = auto()
    SOLDE_HS_A_1 = auto()
    SOLDE_PIQUET = auto()
    SOLDE_PIQUET_A_1 = auto()
    UNKNOWN = auto()


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
        if text_to_import == "":
            return False

        # get all lines as a list
        lines = text_to_import.splitlines()

        self.m_data.piquet_hours = 0
        self.m_data.piquet_minutes = 0
        self.m_data.hr_total_hours = 0
        self.m_data.hr_total_minutes = 0

        soldes_hs_minutes = 0
        soldes_piquet_minutes = 0

        # process the text line by line. and get the type of line (_get_type_of_line).
        for index, line in enumerate(lines):

            if self._get_type_of_line(line) == InfoLineType.ANNUALISATION:
                self.m_data.a_hours, self.m_data.a_minutes = TimeConverter.from_total_minutes(self._get_minutes_from_line(lines[index + 1]))

            if self._get_type_of_line(line) == InfoLineType.SOLDE_VACANCES:
                self.m_data.vac_hours, self.m_data.vac_minutes = TimeConverter.from_total_minutes(self._get_minutes_from_line(lines[index + 1]))

            if self._get_type_of_line(line) == InfoLineType.SOLDE_HS:
                soldes_hs_minutes += self._get_minutes_from_line(lines[index + 1])

            if self._get_type_of_line(line) == InfoLineType.SOLDE_HS_A_1:
                soldes_hs_minutes += self._get_minutes_from_line(lines[index + 1])

            if self._get_type_of_line(line) == InfoLineType.SOLDE_PIQUET:
                soldes_piquet_minutes += self._get_minutes_from_line(lines[index + 1])

            if self._get_type_of_line(line) == InfoLineType.SOLDE_PIQUET_A_1:
                soldes_piquet_minutes += self._get_minutes_from_line(lines[index + 1])

        self.m_data.piquet_hours, self.m_data.piquet_minutes = TimeConverter.from_total_minutes(soldes_piquet_minutes)
        self.m_data.hr_total_hours, self.m_data.hr_total_minutes = TimeConverter.from_total_minutes(soldes_hs_minutes)
        return True

    def _get_minutes_from_line(self, line: str) -> int:
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

    def _get_type_of_line(self, line: str):
        """ Convert a line into a type. following values are supported:
            Annualisation
            Solde Vacances
            Solde HS
            Solde HS A-1
            Solde piquet
            Solde piquet A-1
            The function returns an enumeration of the type of line.
        """
        line_types = {
            "Annualisation": InfoLineType.ANNUALISATION,
            "Solde Vacances": InfoLineType.SOLDE_VACANCES,
            "Solde HS": InfoLineType.SOLDE_HS,
            "Solde HS A-1": InfoLineType.SOLDE_HS_A_1,
            "Solde piquet": InfoLineType.SOLDE_PIQUET,
            "Solde piquet A-1": InfoLineType.SOLDE_PIQUET_A_1,
        }

        return line_types.get(line.strip(), InfoLineType.UNKNOWN)

    def get_processed_data(self) -> InfoData:
        return self.m_data
