import statistics

def CalculateSharpe(portfolio, notRisk=0.0):
    risk = 0.0
    for fund in portfolio.Funds:
        arr = []
        for stat in fund.Statistics:
            for month in stat.MonthPerform:
                arr.append(month.Perfomance)
        if len(arr) > 0:
            risk += Risk(arr, fund.Weight)
            fund.NumbersPeriod = list(arr)
    perfomance = Perfomance(portfolio.Funds)
    portfolio.SharpeRatio = (perfomance-notRisk) / risk
    portfolio.Perfomance = perfomance
    portfolio.Risk = risk

def Perfomance(funds):
    portRes = 0.0
    for fund in funds:
        perfPeriod = 1.0
        for num in fund.NumbersPeriod:
            perfPeriod *= (1 + num)
        res = float(perfPeriod)
        if res < 0:
            return 0.0
        res **= 1 / len(fund.NumbersPeriod)
        res -= 1
        res *= fund.Weight
        portRes += res
    return portRes

def Risk(numbers, weight):
    return statistics.stdev(numbers) * weight