#Uses electricity LCI data from electricitylci package for one eGRID subregion 'CAMX'
#Converting processes from pandas df to dictionary to openLCA schema json-ld using elci native methods
#electricitylci available at https://github.com/usepa/electricitylci

import pandas as pd
import electricitylci as elci

model_name = 'ELCI_1'
output_dir = 'data-background/'
#Creating the generation and generation mix database is slow, so just load the stored database for model 'ELCI_1'
gen_df = pd.read_csv(output_dir+model_name+'_all_gen_db.csv')
genmix_df = pd.read_csv(output_dir+model_name+'_all_gen_mix_db.csv')

#Create surplus pool and consumption mixes for all regions in dictionary format
sur_con_mix_dict = elci.write_surplus_pool_and_consumption_mix_dict()
#Create final distribution to end user processes
dist_dict = elci.write_distribution_dict()

#Subset them only for CAMX egrid subregion
CAMX_gen_df = gen_df[gen_df['Subregion']=='CAMX']
CAMX_genmix_df = genmix_df[genmix_df['Subregion']=='CAMX']

CAMX_sur_con_mix_names = ['SurplusPoolWECC','ConsumptionCAMX']
CAMX_sur_con_mix_dict = {k:v for k,v in sur_con_mix_dict.items() if k in CAMX_sur_con_mix_names}

CAMX_dist_dict = {}
CAMX_dist_dict['DistributionCAMX'] = dist_dict['DistributionCAMX']

#Write dataframes to dictionaries using elci function
#Each record in the gen dataframe becomes an exchange in a process, where processes are Subregion-FuelCategory aggregations of records
CAMX_gen_dict = elci.write_generation_process_database_to_dict(CAMX_gen_df)
#Each record in the genmix dataframe becomes an exchange in a process, where processes are Subregion aggregations of records
CAMX_genmix_dict = elci.write_generation_mix_database_to_dict(CAMX_genmix_df)

#Combine processes from 4 stages of electricity life cycle into 1 dictionary
CAMX_combined = {**CAMX_gen_dict,**CAMX_genmix_dict,**CAMX_sur_con_mix_dict,**CAMX_dist_dict}

#Uses olca-pyi to write dictionary into olca objects and store them in .zip
from electricitylci.olca_jsonld_writer import write as write_jsonld
write_jsonld(CAMX_combined,'CAMX_jsonld.zip')