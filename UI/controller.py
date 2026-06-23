import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_retailer = None

    def fillDropdowns(self):
        years = self._model.getYears()
        brands = self._model.getBrands()
        retailers = self._model.getRetailers()

        for y in years:
            self._view.dd_year.options.append(ft.dropdown.Option(str(y)))

        for b in brands:
            self._view.dd_brand.options.append(ft.dropdown.Option(b))

        for r in retailers:
            self._view.dd_retailer.options.append(
                ft.dropdown.Option(
                    key=r.Retailer_code, text=r.Retailer_name, data=r, on_click=self.read_retailer
                ))

        self._view.update_page()

    def read_retailer(self, e):
        self._selected_retailer = e.control.data
        print(self._selected_retailer.Retailer_name)

    def handle_top_vendite(self, e):
        year = self._view.dd_year.value
        brand = self._view.dd_brand.value

        if year == "Nessun filtro":
            year = None

        if brand == "Nessun filtro":
            brand = None

        retailer = None

        if self._selected_retailer is not None:
            retailer = self._selected_retailer.Retailer_code

        result = self._model.getTopSales(year, brand, retailer)

        self._view.txt_result.controls.clear()

        for row in result:
            self._view.txt_result.controls.append(
                ft.Text(f"Data: {row['Date']}; Ricavo: {row['Revenue']:.2f}; Retailer: {row['Retailer_code']}; Product: {row['Product_number']}"))

        self._view.update_page()

    def handle_analizza_vendite(self, e):
        year = self._view.dd_year.value
        brand = self._view.dd_brand.value

        if year == "Nessun filtro":
            year = None

        if brand == "Nessun filtro":
            brand = None

        retailer = None

        if self._selected_retailer is not None:
            retailer = self._selected_retailer.Retailer_code

        result = self._model.getSalesStats(year, brand, retailer)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Statistiche vendite:"))
        self._view.txt_result.controls.append(
            ft.Text(f"Giro d'affari: {result['fatturato']:.2f}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero vendite: {result['num_vendite']}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero retailers coinvolti: {result['num_retailers']}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero prodotti coinvolti: {result['num_prodotti']}"))

        self._view.update_page()
