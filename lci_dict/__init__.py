import time
from lci_dict.globals import *
from lci_dict.olca_jsonld_writer import write
import olca.units as units

def create_flow(name,flowtype='PRODUCT_FLOW'):
    ar = dict()
    ar['flowType'] = flowtype
    ar['flowProperties']=''
    ar['name'] = name
    ar['id'] = ''
    if (flowtype=='ELEMENTARY_FLOW'):
        ar['category'] = 'Elementary flows/'
    elif (flowtype == 'PRODUCT_FLOW'):
        ar['category'] = default_product_flow_category
    elif flowtype == 'WASTE_FLOW':
        ar['category'] = 'Waste flows/'
    return ar

def create_process(name, exchanges_list):
    ar = dict()
    ar['@type'] = 'Process'
    ar['allocationFactors']=''
    ar['defaultAllocationMethod']=''
    ar['exchanges']= exchanges_list;
    ar['location']= location(default_location)
    ar['parameters']=''
    ar['processDocumentation']=''
    ar['processType']='UNIT_PROCESS'
    ar['name'] = name
    ar['category'] = naics_category
    ar['description'] = ''
    return ar;

def process_doc_creation():
    global year;
    ar = dict()
    ar['timeDescription'] = ''
    ar['validUntil'] = ''
    ar['validFrom'] = ''
    ar['technologyDescription'] = ''
    ar['dataCollectionDescription'] = metadata['DataCollectionPeriod']
    ar['completenessDescription'] = metadata['DataCompleteness']
    ar['dataSelectionDescription'] = metadata['DataSelection']
    ar['reviewDetails'] = metadata['DatasetOtherEvaluation']
    ar['dataTreatmentDescription'] = metadata['DataTreatment']
    ar['inventoryMethodDescription'] = metadata['LCIMethod']
    ar['modelingConstantsDescription'] = metadata['ModellingConstants']
    ar['reviewer'] = metadata['Reviewer']
    ar['samplingDescription'] = metadata['SamplingProcedure']
    ar['sources'] = ''
    ar['restrictionsDescription'] = metadata['AccessUseRestrictions']
    ar['copyright'] = False
    ar['creationDate'] = time.time()
    ar['dataDocumentor'] = metadata['DataDocumentor']
    ar['dataGenerator'] = metadata['DataGenerator']
    ar['dataSetOwner'] = metadata['DatasetOwner']
    ar['intendedApplication'] = metadata['IntendedApplication']
    ar['projectDescription'] = metadata['ProjectDescription']
    ar['publication'] = ''
    ar['geographyDescription'] = ''
    ar['exchangeDqSystem'] = exchangeDqsystem()
    ar['dqSystem'] = processDqsystem()
    # Temp place holder for process DQ scores
    ar['dqEntry'] = None
    return ar;


def create_exchange(name,amount,unit_name,is_reference=False):
    if is_reference:
        bool_input = False
    else:
        bool_input = True
    ar = dict()
    ar['internalId'] = ''
    ar['@type'] = 'Exchange'
    ar['avoidedProduct'] = False
    ar['flow'] = create_flow(name)
    ar['flowProperty'] = ''
    ar['input'] = bool_input
    ar['quantitativeReference'] = is_reference
    ar['baseUncertainty'] = None
    ar['provider'] = ''
    ar['amount'] = float(amount)
    ar['unit'] = create_unit(default_unit_name)
    ar['pedigreeUncertainty'] = ''
    ar['comment'] = ''
    ar['uncertainty'] = None
    return ar;

def create_unit(unt):
    ar = dict()
    ar['internalId']= units.unit_ref(unt).id
    ar['@type']='Unit'
    ar['name'] = unt
    return ar

def location(region):
    ar = dict()
    ar['id'] = ''
    ar['type'] = 'Location'
    ar['name'] = region
    return ar

def exchangeDqsystem():
    ar = dict()
    ar['@type'] = 'DQSystem'
    ar['@id'] = 'd13b2bc4-5e84-4cc8-a6be-9101ebb252ff'
    ar['name'] = 'US EPA - Flow Pedigree Matrix'
    return ar

def processDqsystem():
    ar = dict()
    ar['@type'] = 'DQSystem'
    ar['@id'] = '70bf370f-9912-4ec1-baa3-fbd4eaf85a10'
    ar['name'] = 'US EPA - Process Pedigree Matrix'
    return ar


def write_olca_jsonld(dict, file_path):
    return(write(dict, file_path))

