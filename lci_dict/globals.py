import pandas as pd
import os

try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'lci_dict/'

outputpath = modulepath + 'output/'

bdata_folder = modulepath + '../data-background/'
default_location = 'US'
naics_category = 'NAICS-2/NAICS-4'
default_product_flow_category = ''

default_unit_name = 'Item(s)'

#Read in general metadata to be used by all processes
metadata = pd.read_csv(bdata_folder + 'process_metadata_template.csv')

