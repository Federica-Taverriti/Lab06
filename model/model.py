from database.DAO import DAO

class Model:
    def __init__(self):
        self._sales = DAO.getAllSales()

    def getYears(self):
        return DAO.getYears()

    def getBrands(self):
        return DAO.getBrands()

    def getRetailers(self):
        return DAO.getRetailers()

    #def getTopSales(self, year=None, brand=None, retailer=None):
        #filtered = []

        #for s in self._sales:
            #if year is not None:
                #if s.Date.year != int(year):
                    #continue

            #if brand is not None:
                #if s.Product_brand != brand:
                    #continue

            #if retailer is not None:
                #if s.Retailer_code != retailer.Retailer_code:
                   # continue

            #filtered.append(s)

        #filtered.sort(key=lambda x: x.getRevenue(), reverse=True)
        #return filtered[:5]

    def getTopSales(self, year, brand, retailer):
        return DAO.getTopSales(year, brand, retailer)

    def getSalesStats(self, year, brand, retailer):
        return DAO.getSalesStats(year, brand, retailer)