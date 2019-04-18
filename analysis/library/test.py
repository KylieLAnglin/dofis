def all2018districts(data):
    # statistics from: https://tea.texas.gov/communications/pocket-edition/
    # 1200
    # TODO change to exact number of districts which should be in dataset.
    correct = ((data[data.year == 2018].district.nunique() < 1205) & (
                data[data.year == 2018].district.nunique() > 1200))
    return correct


def alldois(data):
    # 824 in dataset as of April 10, 2019
    # TODO why 824 not 841?
    data = data[data.doi == True]
    correct = ((data.district.nunique() > 820) & (data.district.nunique() <= 824))
    return correct

def alleligible(data):
    # 929
    # TODO confirm
    data = data[data.always_eligible == True]
    data = data[data.year == 2018]
    correct = ((data.district.nunique() >= 927) & (data.district.nunique() <= 931))
    return correct

def onlyeligible(data):
    # 929
    # TODO confirm
    correct = ((data.district.nunique() >= 924) & (data.district.nunique() <= 930))
    return correct

def math2018correct(data):
    # 1578 but not a district average
    # stats from:https://tea.texas.gov/Student_Testing_and_Accountability/Testing/State_of_Texas_Assessments_of_Academic_Readiness_(STAAR)/STAAR_Statewide_Summary_Reports_2017-2018/
    data = data[data.year == 2018]
    ave = data.m_5th_avescore.sum() / len(data.m_5th_avescore)
    correct = ((ave > 1570) & (ave< 1620))
    return correct

def allwithyears(data):
    correct = ((data.district.nunique() >= 874) & (data.district.nunique() <= 880))
    return correct
