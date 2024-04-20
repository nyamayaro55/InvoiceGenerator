from xmlunittest import XmlTestMixin
import datetime
from tempfile import NamedTemporaryFile

from InvoiceGenerator.api import Client, Creator, Invoice, Item, Provider
from InvoiceGenerator.pohoda import SimpleInvoice


class TestBaseInvoice(XmlTestMixin):
    def setup_objects(self):
        provider = Provider('Pupik')
        provider.address = 'Kubelikova blah blah blah'
        provider.zip_code = '12655465'
        provider.city = 'Frantisek'
        provider.vat_id = 'CZ8590875682'
        provider.ir = '785684523'
        provider.email = 'email@email.com'
        provider.bank_account = '2600420569'
        provider.bank_code = '2010'
        provider.bank_name = 'RB'
        provider.note = u'zapsaná v obchodním rejstříku vedeném městským soudem v Praze,\noddíl C, vložka 176551'

        client = Client('Kkkk')
        client.summary = 'Bla blah blah'
        client.address = 'Kubelikova blah blah blah'
        client.zip_code = '12655465'
        client.city = 'Frantisek'
        client.vat_id = 'CZ8590875682'
        client.ir = '785684523'
        client.phone = '785684523'
        client.email = 'email@email.com'
        client.note = u'zapsaná v obchodním rejstříku vedeném městským soudem v Praze,\noddíl C, vložka 176551'

        invoice = Invoice(client, provider, Creator('blah'))
        return invoice

    def test_required_args(self):
        with self.assertRaises(AssertionError):
            SimpleInvoice('Invoice')
        invoice = self.setup_objects()
        SimpleInvoice(invoice)

    def test_generate(self):
        invoice = self.setup_objects()
        invoice.use_tax = True
        invoice.title = u"Testovací faktura"
        invoice.add_item(Item(32, '600.6', description=u"Krátký popis", tax=15))
        invoice.add_item(Item(32, '2.5', tax=21))
        invoice.add_item(
            Item(
                5, '25.42',
                description=u"Dlouhý popis blah blah blah blah blah blah blah blah blah blah blah "
                            u"blah blah blah blah blah blah blah blah blah blah blah blah blah blah "
                            u"blah blah blah blah blah blah blah blah blah blah blah",
                tax=21,),)
        [invoice.add_item(Item(5, '25.42', description=u"Popis", tax=0)) for _ in range(25)]
        invoice.specific_symbol = 666
        invoice.taxable_date = datetime.date.today()
        invoice.variable_symbol = '000000001'
        invoice.number = 'F20140001'
        invoice.payback = datetime.date.today()
        invoice.currency = u'Kč'
        invoice.currency_locale = 'cs_CZ.UTF-8'
        invoice.rounding_result = True

        with NamedTemporaryFile(delete=False) as tmp_file:
            SimpleInvoice(invoice).gen(tmp_file.name)
            xml_string = tmp_file.read().decode('utf-8')

        xpath_values = [
            ('./dataPack/dataPackItem/invoice/partnerIdentity/address/street/text()', 'Kubelikova blah blah blah'),
            ('./dataPack/dataPackItem/invoice/invoiceHeader/number/numberRequested/text()', 'F20140001'),
            ('./dataPack/dataPackItem/invoice/invoiceDetail/invoiceItem/text/text()', 'Popis'),
            ('./dataPack/dataPackItem/invoice/invoiceSummary/priceLow/text/text()', '22102.080'),
            ('./dataPack/dataPackItem/invoice/invoiceSummary/priceHighVAT/text/text()', '43.4910'),
        ]
        for xpath, expected_value in xpath_values:
            self.assertXpathValues(xpath, expected_value)
