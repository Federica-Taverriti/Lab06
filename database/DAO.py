from database.DB_connect import DBConnect
from model.retailer import Retailer
from model.sale import Sale


class DAO():

    @staticmethod
    def getYears():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor()

        query = """SELECT DISTINCT YEAR(Date)
                    FROM go_daily_sales
                    ORDER BY YEAR(Date)"""

        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getBrands():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor()

        query = """SELECT DISTINCT Product_brand
                    FROM go_products
                    ORDER BY Product_brand"""

        cursor.execute(query)

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
                    FROM go_retailers
                    ORDER BY Retailer_name"""

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllSales():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT ds.*, p.Product_brand
                    FROM go_daily_sales ds, go_products p, go_retailers r 
                    WHERE ds.Product_number = p.Product_number
                    AND ds.Retailer_code = r.Retailer_code"""

        cursor.execute(query)

        for row in cursor:
            result.append(Sale(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTopSales(year, brand, retailer):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT ds.*, ds.Unit_sale_price * ds.Quantity AS Revenue
                    FROM go_daily_sales ds, go_products p
                    WHERE ds.Product_number = p.Product_number
                    AND YEAR(ds.Date) = COALESCE(%s, YEAR(ds.Date))
                    AND p.Product_brand = COALESCE(%s, p.Product_brand)
                    AND ds.Retailer_code = COALESCE(%s, ds.Retailer_code)
                    ORDER BY Revenue DESC
                    LIMIT 5"""

        cursor.execute(query, (year, brand, retailer))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getSalesStats(year, brand, retailer):

        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """SELECT COALESCE(SUM(ds.Unit_sale_price * ds.Quantity),0)AS fatturato, COUNT(*) AS num_vendite, 
                    COUNT(DISTINCT ds.Retailer_code) AS num_retailers, COUNT(DISTINCT ds.Product_number) AS num_prodotti
                    FROM go_daily_sales ds, go_products p
                    WHERE ds.Product_number = p.Product_number
                    AND YEAR(ds.Date) = COALESCE(%s, YEAR(ds.Date))
                    AND p.Product_brand = COALESCE(%s, p.Product_brand)
                    AND ds.Retailer_code = COALESCE(%s, ds.Retailer_code)"""

        cursor.execute(query, (year, brand, retailer))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result
