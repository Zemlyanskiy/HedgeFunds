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
    while float("{0:.1f}".format(alpha + delta)) < 1.0 and float("{0:.1f}".format(capital - fund.MinInvest * (1 - alpha))) > 0.0:
        newPort = Portfolio()
        newFund = HedgeFund()
        newFund.Name = fund.Name
        newFund.Statistics = fund.Statistics
        newFund.MinInvest = fund.MinInvest
        newFund.SharpeRatioData = fund.SharpeRatioData
        newPort.Funds = []
        for f in portfolio.Funds:
            n = HedgeFund(f.Name, f.SharpeRatioData, f.MinInvest, float(f.Weight))
            n.Statistics = f.Statistics
            newPort.Funds.append(n)
        alpha += delta
        capital -= newFund.MinInvest * (1 - alpha)
        newPort.Capital = float(capital)
        for f in newPort.Funds:
            f.Weight *= alpha
        newFund.Weight = float(1 - alpha)
        newPort.Funds.append(newFund)
        CalculateSharpe(newPort)
        newPorts.append(newPort)

    return newPorts

def isNotInList(funds, name):
    for fund in funds:
        if fund.Name == name:
            return False
    return True

def Main():
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
    #iterations = len(get_list)
    iterations = 10
    delta = 0.1
    portfolio.Funds.append(max(hedgeFundList, key=attrgetter('SharpeRatioData')))
    portfolio.Funds[0].Weight = 1.0
    portfolio.Capital -= portfolio.Funds[0].MinInvest
    CalculateSharpe(portfolio)
    ports = []
    portfolio.Index = 0
    ports.append(portfolio)
    for i in range(0, iterations):
        for index, fund in enumerate(hedgeFundList):
            if isNotInList(portfolio.Funds, fund.Name):
                portfolies = CheckWeights(portfolio, fund, delta)
                if len(portfolies) == 0:
                    continue
                newPortfolio = max(portfolies, key=attrgetter('SharpeRatio'))
                if newPortfolio.SharpeRatio > portfolio.SharpeRatio:
                    portfolio = newPortfolio
        portfolio.Index = i + 1
        ports.append(portfolio)
    rt = []
    for i in range(0, iterations):
        if i < len(ports):
            rt.append(ports[i].SharpeRatio)
        else:
            rt.append(0.0)
    plt.plot(np.arange(iterations), rt)
    plt.xlabel('Iterations')
    plt.ylabel('SharpeRatio')
    print('Remaining Capital: '+str(portfolio.Capital))
    print('SharpeRatio: '+str(portfolio.SharpeRatio))
    print('Risk: '+str(portfolio.Risk))
    print('Perfomance: '+str(portfolio.Perfomance) + '\n')
    wSum = 0.0
    for fund in portfolio.Funds:
        print('FundName: '+fund.Name)
        print('SharpeRatioData: '+str(fund.SharpeRatioData))
        print('Weight: '+str(fund.Weight))
        wSum += fund.Weight
    print(str(wSum))
    plt.show()

if __name__ == "__main__":
    Main()
