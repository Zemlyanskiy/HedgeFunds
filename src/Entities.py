class Portfolio:
    def __init__(self, capital=None, sharpeRatio=None, risk = None, perfomance = None, index = None):
        self.Funds = []
        self.Capital = capital
        self.SharpeRatio = sharpeRatio
        self.Risk = risk
        self.Perfomance = perfomance
        self.Index = index

class HedgeFund:
    def __init__(self, name = None, sharpeRatioData=None, minInvest = None, weight = None):
        self.Name = name
        self.SharpeRatioData = sharpeRatioData
        self.MinInvest = minInvest
        self.Statistics = []
        self.Weight = weight
        self.NumbersPeriod = []

class Statistics:
    def __init__(self, year=None, ytd=None, dd=None):
        self.Year = year
        self.Ytd = ytd
        self.Dd = dd
        self.MonthPerform = []

class MonthPerform:
    def __init__(self, month=None, year=None, perfomance=None):
        self.Month = month
        self.Perfomance = perfomance
        self.Year = year