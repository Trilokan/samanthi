import datetime

year_start = 2018
year_end = 2022


def get_years():
    """ Used in Accounts for getting Periods"""

    data_list = []
    for year in range(year_start, year_end):
        data = "{0}".format(year)
        data_list.append((data, data))

    return data_list


def get_financial_years():
    """ Used in Accounts for getting Periods"""

    data_list = []
    for year in range(year_start, year_end):
        data = "{0} - {1}".format(year, year + 1)
        data_list.append((data, data))

    return data_list


def get_months():
    """ Used in Accounts for getting Periods"""

    data_list = []
    for year in range(year_start, year_end):
        for period in range(1, 12+1):
            month = datetime.date(year, period, 1).strftime('%B')
            data = "{0} {1}".format(month, year)
            data_list.append((data, data))

    return data_list
