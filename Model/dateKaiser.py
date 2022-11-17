from calendar import day_name
from datetime import date

get_month_str = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Aout",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}

class DateKaiser:
    def __init__(self, year, day, month):
        self.year  = year
        self.month = month
        self.day   = day

    def __str__(self) -> str:
        return "{} {} {}".format(abs(self.year), get_month_str[self.month], "BC" if self.year < 0 else "AC")