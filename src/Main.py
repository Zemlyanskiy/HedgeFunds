import sys
from operator import attrgetter
from src.Parser import Parse
from src.SharpeRatio import CalculateSharpe
from src.Entities import Portfolio

def Main():
    #capital = int(sys.argv[1])
    portfolio = Portfolio
    portfolio.Funds = []
    portfolio.Capital = 1000000
    hedgeFundList = Parse()
    hedgeFundList.sort(key=lambda x: x.SharpeRatioData, reverse=True)
    for index, fund in enumerate(hedgeFundList):
        if fund.SharpeRatioData >= 1.0:
            if portfolio.Capital - fund.MinInvest <= 0:
                break
            if len(fund.Statistics)>0:
                portfolio.Capital -= fund.MinInvest
                portfolio.Funds.append(fund)
    portfolio.Funds[0].Weight = 1.0
    for index in range(1, len(portfolio.Funds)):
        portfolio.Funds[index].Weight = 0.0
    CalculateSharpe(portfolio)
    portfolies = []
    while round(portfolio.Funds[0].Weight - 0.001, 1) >= 0.0:
        for index in range(1, len(portfolio.Funds)):
            portfolio.Funds[0].Weight -= 0.1
            portfolio.Funds[index].Weight += 0.1
        CalculateSharpe(portfolio)
        portfolies.append(portfolio)
    portfolio = max(portfolies, key=attrgetter('SharpeRatio'))
    print('Capital: '+str(portfolio.Capital))
    print('SharpeRatio: '+str(portfolio.SharpeRatio))
    print('Risk: '+str(portfolio.Risk))
    print('Sharpe: '+str(portfolio.Perfomance))
    for fund in portfolio.Funds:
        print('FundName: '+fund.Name)
        print('SharpeRatioData: '+str(fund.SharpeRatioData))
        print('Weight: '+str(fund.Weight))

if __name__ == "__main__":
    Main()
