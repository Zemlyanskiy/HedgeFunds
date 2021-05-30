import sys
from operator import attrgetter
from src.Parser import Parse
from src.SharpeRatio import CalculateSharpe
from src.Entities import Portfolio, HedgeFund
import numpy as np
import matplotlib.pyplot as plt

def CheckWeights(portfolio, fund, delta):
    alpha = 0.0
    capital = float(portfolio.Capital)
    newPorts = []
    while float("{0:.1f}".format(alpha + delta)) < 1.0 and float("{0:.1f}".format(capital - fund.MinInvest * alpha)) > 0.0:
        newPort = Portfolio()
        newFund = HedgeFund()
        newFund.Name = fund.Name
        newFund.Statistics = list(fund.Statistics)
        newFund.MinInvest = fund.MinInvest
        newFund.SharpeRatioData = fund.SharpeRatioData
        newPort.Funds = []
        for f in portfolio.Funds:
            n = HedgeFund(f.Name, f.SharpeRatioData, f.MinInvest, float(f.Weight))
            newPort.Funds.append(n)
        newPort.Capital = portfolio.Capital
        alpha += delta
        capital -= newFund.MinInvest * alpha
        for f in newPort.Funds:
            f.Weight -= alpha / len(newPort.Funds)
        newFund.Weight = float(alpha)
        newPort.Funds.append(newFund)
        CalculateSharpe(newPort)
        newPorts.append(newPort)

    return newPorts

def Main():
    #capital = int(sys.argv[1])
    iterations = 5
    portfolio = Portfolio()
    portfolio.Funds = []
    portfolio.Capital = 1000000
    hedgeFundList = Parse()
    hedgeFundList.sort(key=lambda x: x.SharpeRatioData, reverse=True)
    get_list = []
    for h in hedgeFundList:
        if len(h.Statistics) >= 2 and h.MinInvest is not None:
            h.Statistics = h.Statistics[:2]
            get_list.append(h)
    hedgeFundList = get_list
    portfolio.Funds.append(max(hedgeFundList, key=attrgetter('SharpeRatioData')))
    portfolio.Funds[0].Weight = 1.0
    portfolio.Capital -= portfolio.Funds[0].MinInvest
    CalculateSharpe(portfolio)
    ports=[]
    delta = 0.1
    for i in range(0, iterations):
        for index, fund in enumerate(hedgeFundList):
            if portfolio.Funds.count(fund) == 0:
                portfolies = CheckWeights(portfolio, fund, delta)
                newPortfolio = max(portfolies, key=attrgetter('SharpeRatio'))
                if newPortfolio.SharpeRatio > portfolio.SharpeRatio:
                    portfolio = newPortfolio
                    newPortfolio.Index = i
                    ports.append(newPortfolio)
        delta *= 0.1
    rt = []
    for i in range(0, iterations):
        if i < len(ports):
            print('SharpeRatio: '+str(ports[i].SharpeRatio))
            rt.append(ports[i].SharpeRatio)
        else:
            rt.append(0.0)
    rt.sort()
    plt.plot(np.arange(iterations), rt)
    plt.xlabel('Iterations')
    plt.ylabel('SharpeRatio')
    plt.show()
    #print('Capital: '+str(portfolio.Capital))
    #print('SharpeRatio: '+str(portfolio.SharpeRatio))
    #print('Risk: '+str(portfolio.Risk))
    #print('Perfomance: '+str(portfolio.Perfomance) + '\n')
    #for fund in portfolio.Funds:
    #    print('FundName: '+fund.Name)
    #    print('SharpeRatioData: '+str(fund.SharpeRatioData))
    #    print('Weight: '+str(fund.Weight))
        #for stat in fund.Statistics:
        #    for month in stat.MonthPerform:
        #        print('Month '+str(month.Month)+' Year '+str(month.Year)+' Perf ' + str(month.Perfomance))

if __name__ == "__main__":
    Main()
