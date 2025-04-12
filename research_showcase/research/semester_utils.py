from datetime import date

SEMESTER_PATTERNS = {
    'Spring': {'start_month': 1, 'start_day': 10, 'end_month': 5, 'end_day': 10},
    'Summer': {'start_month': 5, 'start_day': 11, 'end_month': 8, 'end_day': 15},
    'Fall': {'start_month': 8, 'start_day': 16, 'end_month': 12, 'end_day': 15},
    'Winter': {'start_month': 12, 'start_day': 16, 'end_month': 1, 'end_day': 9}
}

def generate_semesters(start_year, end_year):
    semesters = {}
    
    for year in range(start_year, end_year + 1):
        for season, pattern in SEMESTER_PATTERNS.items():
            # Handle winter semester crossing year boundary
            if season == 'Winter':
                end_year = year + 1
            else:
                end_year = year
                
            semesters[f'{season} {year}'] = {
                'start': date(year, pattern['start_month'], pattern['start_day']),
                'end': date(end_year, pattern['end_month'], pattern['end_day'])
            }
    
    return semesters

def get_semester_choices(start_year, end_year):
    semesters = generate_semesters(start_year, end_year)
    # Sort by year then by standard season order
    season_order = {'Fall': 0, 'Winter': 1, 'Spring': 2, 'Summer': 3 }
    return [(key, key) for key in sorted(
        semesters.keys(),
        key=lambda x: (int(x.split()[1]), season_order[x.split()[0]])
    )]

# Pre-generate common data
CURRENT_YEAR = date.today().year
SEMESTERS = generate_semesters(CURRENT_YEAR - 5, CURRENT_YEAR + 2)
SEMESTER_CHOICES = get_semester_choices(CURRENT_YEAR - 5, CURRENT_YEAR + 2)