PHI = (1 + 5**0.5) / 2
WIDTH = int(600)
HEIGHT = int(500 * PHI)

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

month_scheme = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

week_scheme = [4, 0, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2]

month_dict = {}

for i in range(len(months)):

    month_dict[months[i]] = month_scheme[i]

week_dict = {}

for i in range(len(months)):

    week_dict[months[i]] = week_scheme[i]
