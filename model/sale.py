from dataclasses import dataclass
from datetime import date


@dataclass
class Sale:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: date
    Quantity:int
    Unit_price: float
    Unit_sale_price:float
    Product_brand: str

    def getRevenue(self):
        return self.Unit_sale_price * self.Quantity