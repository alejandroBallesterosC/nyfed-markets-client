
import requests
from datetime import date
from io import StringIO
import csv
import json

class IllegalArgumentError(ValueError):
    pass

class NYFedMarketsClient:
    '''API Docs: https://markets.newyorkfed.org/static/docs/markets-api.html'''
    POSSIBLE_FORMATS = ['json', 'csv', 'xml', 'xlsx']
    BASE_URL = 'https://markets.newyorkfed.org/api'
    
    def __init__(self):
        pass
        
    def handleResponse(self, response, fType='json'):
        response.raise_for_status()
        if fType == 'json':
            return response.json()
        elif fType in self.POSSIBLE_FORMATS:
            return response.text
        else:
            raise IllegalArgumentError('Format Type not valid Format Type')

    def stringToCsv(self, textString, fPath='file.csv'):
        buffer = StringIO(textString)
        reader = csv.reader(buffer, skipinitialspace=True)
        with open(fPath, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(reader)
            out_file.close()

    def saveJson(self, dict, fpath='file.json'):
        json_object = json.dumps(dict, indent=4) # Serialize JSON
        with open(fPath, "w") as outfile: # Write to file
            outfile.write(json_object)
            outfile.close()

class AgencyMortgageBackedSecurities(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/ambs'
    
    def __init__(self):
        pass
        
    def getCurrentDateOperations(self, operation='all', status='announcements',
                                     include='summary', fType='json'):
        '''Returns the latest AMBS operation Announcements or Results for the current day.'''
        
        endPt = f'/{operation}/{status}/{include}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType) 
    
    def getLastTwoWeeksOperations(self, operation='all', include='summary', fType='json'):
        '''Returns the last two weeks AMBS operations Results.'''
        
        endPt = f'/{operation}/results/{include}/lastTwoWeeks.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getLastNOperations(self, operation='all', include='summary', number=10, fType='json'):
        '''Returns the last N number of AMBS operations Results.'''
        
        endPt = f'/{operation}/results/{include}/last/{number}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getFilteredOperations(self, operation='all', include='summary', fType='json', params=None):
        '''Returns Filtered AMBS Operation Results. Params: startDate, endDate, securities,
        cusip, desc.'''
        
        endPt = f'/{operation}/results/{include}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
    
class CentralBankLiquiditySwaps(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/fxs'

    def __init__(self):
        pass

    def getCurrentDateOperations(self, operationType='all', fType='json'):
        '''Returns the latest Liquidity Swaps operation Results posted on current day.'''
        
        endPt = f'/{operationType}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastNOperations(self, operationType='usdollar', number=10, fType='json'):
        '''Returns the last N number of Liquidity Swaps operations Results.'''
        
        endPt = f'/{operationType}/last/{number}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredOperations(self, operationType='all', fType='json', params=None):
        '''Returns Filtered Liquidity Swaps operation Results. Params: startDate,
        endDate, dateType, counterparties.'''
        
        endPt = f'/{operationType}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
    def getCounterparties(self, fType='json'):
        '''Returns Counterparties of Liquidity Swaps operations.'''
        
        endPt = f'/list/counterparties.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)


class Guidesheets(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/guidesheets'
    
    def __init__(self):
        pass
    
    def getCurrentGuidesheet(self, guidesheetType='si', fType='json'):
        '''Returns the latest Guide Sheet.'''
        
        endPt = f'/{guidesheetType}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getPreviousGuidesheet(self, guidesheetType='si', fType='json'):
        '''Returns the previous Guide Sheet.'''
        
        endPt = f'/{guidesheetType}/previous.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
class PrimaryDealer(NYFedMarketsClient):
    BASE_PD_URL = NYFedMarketsClient.BASE_URL + '/pd'
    BASE_MS_URL = NYFedMarketsClient.BASE_URL + '/marketshare'
    TODAY = date.today().strftime('%Y-%m-%d')

    def __init__(self):
        pass
    
    def getLatestSurveyBySb(self, seriesbreak, fType='json'):
        '''Returns the latest Survey results by series break for a time series.'''
        
        endPt = f'/latest/{seriesbreak}.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getAllSurveys(self):
        '''Returns all Survey results in csv format.'''
        
        endPt = '/get/all/timeseries.csv'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType='csv')
    
    def getSurveyDesc(self, fType='json'):
        '''Returns Description of timeseries/keyids.'''
        
        endPt = f'/list/timeseries.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getSurveyAsOfDates(self, fType='json'):
        '''Returns all As Of Dates with respective Series Break.'''
        
        endPt = f'/list/asof.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getSurveySeriesbreaks(self, fType='json'):
        '''Returns Series Breaks including Label, Start and End Date.'''
        
        endPt = f'/list/seriesbreaks.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getSurveyByDate(self, date=None, fType='json'):
        '''Returns single date Survey results by As Of date'''

        if not date:
            date = self.TODAY
        endPt = f'/get/asof/{date}.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getSurveyByTs(self, timeseries, fType='json'):
        '''Return Survey results for given timeseries across all Series Breaks.
        To query multiple timeseries, separate each with underscore(_).'''
        
        endPt = f'/get/{timeseries}.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getSurveyByTsAndSb(self, seriesbreak, timeseries, fType='json'):
        '''Return Survey results for given seriesbreak and timeseries. 
        To query multiple timeseries, separate each with underscore(_).'''
        
        endPt = f'/get/{seriesbreak}/timeseries/{timeseries}.{fType}'
        response = requests.get(self.BASE_PD_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getLatestQtrlyMarketShare(self, fType='xml'):
        '''Returns the latest quarterly Primary Dealer Market Share.'''
        
        endPt = f'/qtrly/latest.{fType}'
        response = requests.get(self.BASE_MS_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLatestYTDMarketShare(self, fType='xml'):
        '''Returns the latest year-to-date Market Share.'''
        
        endPt = f'/ytd/latest.{fType}'
        response = requests.get(self.BASE_MS_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
class ReferenceRates(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/rates'
    
    def __init__(self):
        pass
    
    def getLatestRates(self, fType='json'):
        '''Returns the latest secured and unsecured rates.'''
        
        endPt = f'/all/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)


    def getFilteredRates(self, fType='json', params=None):
        '''Returns secured and/or unsecured rates and/or volume. Optional Params: startDate,
        endDate, type.'''
        
        endPt = f'/all/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
        
    def getLatestSecuredRates(self, fType='json'):
        '''Returns the latest secured rates.'''
        
        endPt = f'/secured/all/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastNSecuredRates(self, rateType='sofr', number=10, fType='json'):
        '''Returns the last N number of secured rates.'''
        
        endPt = f'/secured/{rateType}/last/{number}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredSecuredRates(self, rateType='sofr', fType='json', params=None):
        '''Returns filtered secured rates and/or volume. Params: startDate, 
        endDate, type.'''
        
        endPt = f'/secured/{rateType}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
    def getLatestUnsecuredRates(self, fType='json'):
        '''Returns the latest unsecured rates.'''
        
        endPt = f'/unsecured/all/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredUnsecuredRates(self, rateType='effr', fType='json', params=None):
        '''Returns unsecured rates and/or volume. Params: startDate,
        endDate, type'''
        
        endPt = f'/unsecured/{rateType}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
class RepoMarket(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/rp'
    
    def __init__(self):
        pass

    def getCurrentDateOperations(self, operationType='all', method='all', 
                                 status='results', fType='json'):
        '''Returns the latest Repo and/or Reverse Repo operations Announcements or 
        Results for the current day.'''
        
        endPt = f'/{operationType}/{method}/{status}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastTwoWeeksOperations(self, operationType='all', method='all',
                                 fType='json'):
        '''Returns the last two weeks Repo and/or Reverse Repo operations Results.'''
        
        endPt = f'/{operationType}/{method}/results/lastTwoWeeks.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastNOperations(self, operationType='all', method='all', number=10,
                           fType='json'):
        '''Returns the last N number of Repo and/or Reverse Repo operations Results.'''
        
        endPt = f'/{operationType}/{method}/results/last/{number}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredOperations(self, fType='json', params=None):
        '''Returns filtered Repo and/or Reverse Repo operation Results.
        Params: startDate, endDate, '''
        
        endPt = f'/results/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredReverseRepoOperations(self, fType='json', params=None):
        '''Returns filtered Propositions for Reverse Repo operations.
        Params: startDate, endDate'''
        
        endPt = f'/reverserepo/propositions/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
class SecuritiesLending(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/seclending'
    
    def __init__(self):
        pass
    
    def getCurrentDateOperations(self, operation='all', include='details', fType='json'):
        '''Returns the latest Securities Lending operation Results for the current day.'''
        
        endPt = f'/{operation}/results/{include}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getLastTwoWeeksOperations(self, operation='all', include='details', fType='json'):
        '''Returns the last two weeks Securities Lending operation Results and/or Extensions.'''
        
        endPt = f'/{operation}/results/{include}/lastTwoWeeks.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastNOperations(self, operation='all', include='details', number=10, fType='json'):
        '''Returns the last N number of Securities Lending operation Results and/or Extensions.'''
        
        endPt = f'/{operation}/results/{include}/lastTwoWeeks.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredOperations(self, operation='all', include='details', fType='json', params=None):
        '''Returns Securities Lending operation Results and/or Extensions. Params: startDate, endDate,
        cusips, descriptions'''
        
        endPt = f'/{operation}/results/{include}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)
    
class SOMA(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/soma'
    TODAY = date.today().strftime('%Y-%m-%d')
    
    def __init__(self):
        pass
    
    def getLatestAsOfDate(self, fType='json'):
        '''Returns the latest SOMA holdings As Of Date.'''
        
        endPt = f'/asofdates/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getTotalHoldingsBySecurity(self, fType='json'):
        '''Returns Summary Of SOMA holdings for each As of Date and holding type.'''
        
        endPt = f'/summary.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getAllAsOfDates(self, fType='json'):
        '''Returns all SOMA holdings As of Date.'''
        
        endPt = f'/asofdates/list.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastThreeMonthsReleaseAndAsOfDates(self, fType='json'):
        '''Returns the last three months Agency Release and As Of Dates.'''
        
        endPt = f'/agency/get/release_log.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getHoldingsByDate(self, date=None, fType='json'):
        '''Returns a single date SOMA Agency Holdings.'''

        if not date:
            date=self.TODAY
        endPt = f'/agency/get/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getHoldingsByCusip(self, cusip=None, fType='json'):
        '''Returns all SOMA Agency Holdings for a single CUSIP.'''
        
        endPt = f'/agency/get/cusip/{cusip}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
        
    def getHoldingsBySecurityAndDate(self, holdingType='all', date=None, fType='json'):
        '''Returns a single date SOMA Agency Holdings for a Agency holding type.'''
        
        if not date:
            date = self.TODAY
        endPt = f'/agency/get/{holdingType}/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getAgencyDebtWamByDate(self, date=None, fType='json'):
        '''Returns a single date Weighted Average Maturity for Agency Debt.'''
        
        if not date:
            date = self.TODAY
        endPt = f'/agency/wam/agency debts/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastThreeMonthsTreasuryReleaseDates(self, fType='json'):
        '''Returns the last three months Treasury Security Release and As Of Dates.'''
        
        endPt = f'/tsy/get/release_log.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getTreasuryHoldingsByDate(self, date=None, fType='json'):
        '''Returns a single date SOMA Treasury Holdings.'''
        
        if not date:
            date = self.TODAY
        endPt = f'/tsy/get/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)

    def getTreasuryHoldingsByCusip(self, cusip=None, fType='json'):
        '''Returns all SOMA Treasury Holdings for a single CUSIP.'''
        
        endPt = f'/tsy/get/cusip/{cusip}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getTreasuryHoldingsByTypeAndDate(self, holdingType='all', date=None, fType='json'):
        '''Returns a single date SOMA Treasury Holdings for a Treasury holding type and date'''
        
        if not date:
            date = self.TODAY
        endPt = f'/tsy/get/{holdingType}/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getTreasuryHoldingWamByTypeAndDate(self, holdingType='all', date=None, fType='json'):
        '''Returns a single date Weighted Average Maturity for a Treasury holding type.'''
        
        if not date:
            date = self.TODAY
        endPt = f'/tsy/wam/{holdingType}/asof/{date}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getHistoricalMonthlyTreasuryHoldings(self, fType='json'):
        '''Returns all SOMA Treasury Holdings at monthly intervals.'''
        
        endPt = f'/tsy/get/monthly.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    

class TreasuryOperations(NYFedMarketsClient):
    BASE_URL = NYFedMarketsClient.BASE_URL + '/tsy'
    
    def __init__(self):
        pass
    
    def getCurrentDateOperations(self, operation='all', status='results', include='details', 
                                 fType='json'):
        '''Returns the latest Treasury operation Announcements or Results for the current day.'''
        
        endPt = f'/{operation}/{status}/{include}/latest.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastTwoWeeksOperations(self, operation='all', include='details', fType='json'):
        '''Returns the last two weeks Treasury operations Results.'''
        
        endPt = f'/{operation}/results/{include}/lastTwoWeeks.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getLastNOperations(self, operation='all', include='details', number=10, fType='json'):
        '''Returns the last N number of Treasury operations Results.'''
        
        endPt = f'/{operation}/results/{include}/last/{number}.{fType}'
        response = requests.get(self.BASE_URL + endPt)
        return self.handleResponse(response, fType=fType)
    
    def getFilteredOperations(self, operation='all', include='details', fType='json', params=None):
        '''Returns filtered Treasury operation Results. Params: startDate, endDate, securityType,
        cusip, desc'''
        
        endPt = f'/{operation}/results/{include}/search.{fType}'
        response = requests.get(self.BASE_URL + endPt, params=params)
        return self.handleResponse(response, fType=fType)