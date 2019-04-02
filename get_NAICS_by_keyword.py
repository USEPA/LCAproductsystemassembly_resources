#Uses a NAICS lookup webservice to get NAICS info for selected keywords.
#http://www.exchangenetwork.net/data-exchange/naics/
#Limited to keyword in NAICS names

import requests as r
import xml.etree.ElementTree as ET
import pandas as pd

#These words could be gathered from a file. Synonymns could also be found
#Try a couple keywords with matches, and a third without
keywords = ['bolt','photo','haberdashery']
base_url = 'https://ends2.epa.gov/RestProxy/Query?Node=.NetNode2&Dataflow=NAICS&Request=GetNAICSCodesByKeyword_v1.0&Params=CodeSetYear|2012;Keyword|'

candidate_NAICS_by_keyword = pd.DataFrame(columns=cols)

for k in keywords:
    url = base_url+k
    cols = ['keyword','NAICS_Code','NAICS_Name']
    response = r.get(url)
    header = response.headers['content-type']
    #if xml not in header, not results found
    if header.find('xml') > -1:
        response_xml = ET.fromstring(response.content)
        codes = response_xml.findall(".//{http://www.exchangenetwork.net/schema/NAICS/1}Code")
        codes_for_keyword = {}
        codes_for_keyword['keyword'] = k
        for c in codes:
            code = c.find("./{http://www.exchangenetwork.net/schema/NAICS/1}NAICSCodeText")
            codes_for_keyword['NAICS_Code'] = code.text
            code_name = c.find("./{http://www.exchangenetwork.net/schema/NAICS/1}NAICSNameText")
            codes_for_keyword['NAICS_Name'] = code_name.text
            candidate_NAICS_by_keyword = candidate_NAICS_by_keyword.append(codes_for_keyword,ignore_index=True)

#Peek at it
candidate_NAICS_by_keyword