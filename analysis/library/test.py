
# Notes:
# Two districts missing test scores
# 48 districts missing doi year

def allyearsanddistricts(data, just_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]):
    ground_truth = {2012: 1227,
                    2013: 1228,
                    2014: 1227,
                    2015: 1219,
                    2016: 1207,
                    2017: 1203,
                    2018: 1200}
    count_correct = 0
    count_total = len(just_years)
    for yr in just_years:
        if len(data[data.year == yr]) == ground_truth[yr]:
            count_correct = count_correct + 1
        if len(data[data.year == yr]) != ground_truth[yr]:
            print('Year ', yr, 'should have', ground_truth[yr], 'districts. But has ', len(data[data.year == yr]))
    correct = (count_correct == count_total)
    return correct

def allyearsandtpsd(data, just_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]):
    ground_truth = {2012: 1029,
                    2013: 1026,
                    2014: 1025,
                    2015: 1024,
                    2016: 1024,
                    2017: 1023,
                    2018: 1023}
    count_correct = 0
    count_total = len(just_years)
    for yr in just_years:
        if len(data[data.year == yr]) == ground_truth[yr]:
            count_correct = count_correct + 1
        if len(data[data.year == yr]) != ground_truth[yr]:
            print('Year ', yr, 'should have', ground_truth[yr], 'districts. But has ', len(data[data.year == yr]))
    correct = (count_correct == count_total)
    return correct


def alldois(data):
    # 824 in dataset as of April 10, 2019
    data = data[data.doi == True]
    correct = ((data.district.nunique() == 824))
    return correct

def alldoiswithdates(data):
    data = data[data.doi == True]
    data = data[pd.notnull(data.doi_year)]
    correct = ((data.district.nunique() == 777))

def math2018correct(data):
    # 1578 but not a district average
    # stats from:https://tea.texas.gov/Student_Testing_and_Accountability/Testing/State_of_Texas_Assessments_of_Academic_Readiness_(STAAR)/STAAR_Statewide_Summary_Reports_2017-2018/
    data = data[data.year == 2018]
    ave = data.m_5th_avescore.sum() / len(data.m_5th_avescore)
    correct = ((ave > 1570) & (ave< 1620))
    return correct

