import statistics

def CalculateSharpe(portfolio, capit, notRisk=0.0):
    perfomance = 0.0
    risk = 0.0
    for fund in portfolio.Funds:
        arr = []
        for stat in fund.Statistics:
            for month in stat.MonthPerform:
                arr.append(month.Perfomance)
        if len(arr) > 0:
            perfomance += Perfomance(arr, fund.Weight)
            #perfomance = perfomance / capit - 1
            perfomance = pow(perfomance, 1 / len(arr))
            risk += Risk(arr, fund.Weight)
            portfolio.SharpeRatio = (perfomance-notRisk) / risk
            portfolio.Perfomance = perfomance
            portfolio.Risk = risk


def Perfomance(numbers, weight):
    #return float(sum(numbers)) / max(len(numbers), 1) * weight
    perf = 1.0
    for num in numbers:
        perf *= (1 + num)
    #perf = pow(perf, 1 / len(numbers))
    return perf * weight

def Risk(numbers, weight):
    return statistics.stdev(numbers) * weight