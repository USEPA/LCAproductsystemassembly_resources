import pandas as pd

bdata_folder = 'data-background/'
default_location = 'US'
naics_category = '31-33: Manufacturing/3364: Aerospace Product and Parts Manufacturing/'
default_product_flow_category = ''

default_unit_name = 'Item(s)'

olca_units = pd.read_csv(bdata_folder + 'olca_unit_metadata.csv')

#Read in general metadata to be used by all processes
metadata = pd.read_csv(bdata_folder + 'process_metadata_template.csv')

