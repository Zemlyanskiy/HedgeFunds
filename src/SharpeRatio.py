import statistics

def CalculateSharpe(portfolio, notRisk=0.0):
    perfomance = 0.0
    risk = 0.0
    for fund in portfolio.Funds:
        arr = []
        for stat in fund.Statistics:
            for month in stat.MonthPerform:
                arr.append(month.Perfomance)
        if len(arr) > 0:
            perfomance += Perfomance(arr, fund.Weight)
            risk += Risk(arr, fund.Weight)
            portfolio.SharpeRatio = (perfomance-notRisk) / risk
            portfolio.Perfomance = perfomance
            portfolio.Risk = risk


def Perfomance(numbers, weight):
    return float(sum(numbers)) / max(len(numbers), 1) * weight

def Risk(numbers, weight):
    return statistics.stdev(numbers) * weight