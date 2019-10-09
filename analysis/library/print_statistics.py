def print_school_counts(data):
    print("There were 8766 schools in Texas in 2018. Of these 705 were charters.")
    print(data[['district', 'campus', 'year']].groupby(['year']).nunique()[['district', 'campus']])