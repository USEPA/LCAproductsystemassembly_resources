"""
Creates a foreground product system model (PSM) as a Python dictionary without links to background processes for a machine
based on one or more multi-level Bill of Materials (BOM) file(s). The dictionary is written to an openLCA JSON-LD archive
and a summary is created by process.

(https://en.wikipedia.org/wiki/Bill_of_materials) with these fields:
Level - indicates level in assembly, with 0 being higher (integrating all subassemblies/components)
Part Number
PT
QNA
Part Name
Next Assembly
"""

#Get data from BOM data files
import pandas as pd
import lci_dict
import os
import logging as log
import sys

log.basicConfig(level=log.INFO, format='%(levelname)s %(message)s',
                stream=sys.stdout)
data_folder = 'data-foreground/'
output_folder = 'output/'

#Provide a dictionary that define names of Excel files with BOM and number of sheets in each. This could be multiple files
BOM_name_sheets = {'BOM_1':5}  #,'BOM_2':5}

def main():

    assembly_df = pd.DataFrame()
    for k,v in BOM_name_sheets.items():
        BOM_file = data_folder + k + '.xlsx'
        for s in range(v):
            df = pd.read_excel(BOM_file, sheet_name=s)
            log.info('Reading in ' + str(len(df)) + ' rows from sheet ' + str(s) + ' in BOM ' + k)
            df['BOM'] = k
            assembly_df = assembly_df.append(df, ignore_index=True)
        log.info('Created data frame "assembly_df" with assembly info')

    #Convert columns to numeric that should be so
    import numpy as np
    assembly_df['QNA'] = pd.to_numeric(assembly_df['QNA'], errors='coerce')
    assembly_df['Level'] = pd.to_numeric(assembly_df['Level'], errors='coerce')
    assembly_df['Part Name'] = assembly_df['Part Name'].astype('str')
    assembly_df['Part Number'] = assembly_df['Part Number'].astype('str')

    #Create a process dictionary
    log.info('Creating a process dictionary')
    processes_dict = {}
    for index, row in assembly_df.iterrows():
        #Create exchanges for ref flow and all inputs. Determine these based on 'Next Assembly'
        #Subset df for 'next-assembly' to add all as exchanges
        inputs_df = assembly_df[assembly_df['Next Assembly'] == row['Part Number']]

        #Only proceed if there are inputs to this item
        if len(inputs_df) > 0:
            # create a list of exchanges for all these records
            exchanges = []
            # Create ref flow first
            exchanges.append(lci_dict.create_exchange(row['Part Name']+'-'+row['Part Number'], 1, 'Item(s)', is_reference=True))
            input_exchanges = [lci_dict.create_exchange(r['Part Name']+'-'+r['Part Number'], r['QNA'], 'Item(s)') for i, r in inputs_df.iterrows()]
            for e in input_exchanges:
                exchanges.append(e)
            #Create process with exchanges
            process_dict = lci_dict.create_process(row['Part Name']+'-'+row['Part Number'], exchanges)
            processes_dict[row['Part Name']+'-'+row['Part Number']] = process_dict

    #how many processes?
    log.info('Createde dictionary with ' + str(len(processes_dict)) + ' processes.')

    #Summarize
    process_summary_df = pd.DataFrame(columns=['ProcessName','NumExchanges','Cutoffs'])
    for k,v in processes_dict.items():
        a = {}
        a['ProcessName'] = k
        a['NumExchanges'] = len(v['exchanges'])
        #Determine number of cutoffs
        cutoffs = 0
        for e in v['exchanges']:
            f_name = e['flow']['name']
            try:
                processes_dict[f_name]
            except KeyError: #
                cutoffs = cutoffs + 1
        a['Cutoffs'] = cutoffs
        process_summary_df = process_summary_df.append(a,ignore_index=True)

    #Write these processes out to an olca jsonld archive
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    log.info('Writing JSON_LD zip archive to output folder')
    lci_dict.write_olca_jsonld(processes_dict,output_folder+'assemblyPSM.zip')

    process_summary_df.to_csv(output_folder+'assembly_process_summary.csv',index=False)


if __name__ == '__main__':
    main()















