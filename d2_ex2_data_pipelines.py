# ##
# pip install pydantic_extra_types
# pip install pycountry
# ##

# problemă:
# vrem să încărcăm în pandas un excel
# doar dacă am trecut printr-un proces de validare mai întâi.
#
# dar!
# nu vrem să citim fișierul de pe drive de 2 ori !!!!!!!
#
#
# posibilități:
# A.
#   - creăm DataFrame manual, gol
#   - citim fișierul cu openpyxl / xlrd
#   - citim și validăm row-by-row 
#   - la fiecare row valid facem append (concat) manual la DataFrame
#   - dacă găsim eroare de validare, fail-uim tot procesul
#
# B.
#  - citim fișierul cumva ca iterator
#  - cumva, stream-uim în procesul care face validare cu pydantic
#  - în timp ce stream-uim și la pandas


import sys
import openpyxl
import pydantic
import pandas as pd
import typing
from functools import partial

from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha2


# object-relational-mapping style

class Customer(BaseModel):
    Name: str
    Country: CountryAlpha2

# plan:
# data structures, business-to-code datamodel mapping
# operațiuni pe datamodel (băgăm, scoatem bani din cont...)
# loading datasets pe datamodel din csv / excel / combinație cu json
# writing datasets în db / scris rapoarte în csv / json


# pipeline:
# acțiune 1: validation & data (pre-)processing
#            --> objects
# acțiune 2: load the stream into DataFrame


CUSTOMERS_SPREADSHEET = '/tmp/data-test.xlsx'

def load_customers_from_xlsx(path, sheet_num=0):
    """
    loads a spreadsheet of customers
    and yields each row as a `Customer` object
    """
    with open(path, 'br') as fp:
        book = openpyxl.load_workbook(fp, read_only=True, data_only=True)
        sheet = book.worksheets[sheet_num]

        rows = sheet.iter_rows()

        header_row = next(rows)
        header = tuple(c.value for c in header_row)

        for row in rows:
            data = (col.value for col in row)
            yield dict(zip(header, data))

def load_customers_from_csv(path):
    pass
    #for row in csv.DictReader(fp):
    #    yield row


def validate_customers_pipeline(dataset, error_handler=None):
    for row in dataset:
        try:
            customer = Customer(**row)
        except pydantic.ValidationError as e:
            # do something with the exception
            #raise e
            if error_handler is not None:
                error_handler(e.errors())
        else:
            yield customer
        finally:
            # do some clean-up
            # dbconnection.close() # (dacă nu eram în context manager)
            pass


def mk_dataframe_from_customer_dataset(customers):
    return pd.DataFrame.from_records(
        customer.model_dump()
        for customer in customers
    )

### version 1:
"""
error_printer = partial(print, "[err]", file=sys.stderr)

customer_rows = load_customers_from_xlsx(CUSTOMERS_SPREADSHEET)

customer_objects = validate_customers_pipeline(customer_rows,
                                               error_handler=error_printer)
print(
    mk_dataframe_from_customer_dataset(customer_objects)
)
"""

class CustomersPipelineHandler:
    def __init__(self, dataset):
        self.dataset = dataset
        self.errors = []

    def __iter__(self):
        return self

    def __next__(self):
        for row in self.dataset:
            try:
                customer = Customer(**row)
            except pydantic.ValidationError as e:
                self.errors.append(e)
            else:
                return customer
            finally:
                # do some clean-up
                # dbconnection.close() # (dacă nu eram în context manager)
                pass

        raise StopIteration()

### version 2:
"""
customer_rows = load_customers_from_xlsx(CUSTOMERS_SPREADSHEET)
customer_collection = CustomersPipelineHandler(customer_rows)

print(
    mk_dataframe_from_customer_dataset(customer_collection)
)

if customer_collection.errors:
    print("has errors!")
    for e in customer_collection.errors:
        print("»", e)
"""

### version 3:
### we go OOP, and we go elegantic

class BasePassthroughAction:
    def __init__(self, dataset):
        self.dataset = iter(dataset)
        self.data = None

    def __iter__(self):
        return self
    
    def __next__(self):
        item = next(self.dataset)
        return self.handle_item(item)
    
    def handle_item(self, item):
        return item

class DistinctCountryLoggerPassthroughAction(BasePassthroughAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = set()

    def handle_item(self, item):
        self.data.add(item.Country)
        return item


actions = [
    load_customers_from_xlsx,
    CustomersPipelineHandler,
    DistinctCountryLoggerPassthroughAction,
    mk_dataframe_from_customer_dataset,
]


class PipelineAction(typing.NamedTuple):
    action: typing.Callable
    input:  typing.Any
    output: typing.Any


class Pipeline:
    def __init__(self, entry_data, actions):
        self.actions = actions
        self.results = []

        self.last_result = entry_data

    def run(self):
        for action in self.actions:
            intermediary_result = action(self.last_result)

            self.results.append(PipelineAction(
                action, self.last_result, intermediary_result,
            ))

            self.last_result = intermediary_result

        return self.last_result

ppl = Pipeline(CUSTOMERS_SPREADSHEET, actions)
result = ppl.run()

print("===== final result =====")
print(result)
print("========================")

print("\n")

print("===== ran actions: =====")
for rez in ppl.results:
    _info = [rez.action.__name__]
    if hasattr(rez.output, 'errors') and rez.output.errors:
        _info.append('[has errors]')
    if hasattr(rez.output, 'data') and rez.output.data:
        _info.append('[has data]')

    print("»", *_info)
print("========================")

print("\n")

print("======== datas: ========")
for rez in ppl.results:
    if hasattr(rez.output, 'data') and rez.output.data:
        print ("»»»", rez.action)
        print(rez.output.data)
print("========================")

print("\n")

print("======== errors: ========")
for rez in ppl.results:
    if hasattr(rez.output, 'errors') and rez.output.errors:
        print ("»»»", rez.action)
        print(rez.output.errors)
print("========================")
