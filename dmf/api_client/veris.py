from .client import SsnApiClient
from dicttoxml import dicttoxml
from xml.etree.ElementTree import fromstring
from xmljson import parker
import pdb
import requests

class VerisSsnClient(SsnApiClient):
    def __init__(self, app_config):
        self.default_query = {
            'UserID': app_config['USER_ID'],
            'Password': app_config['PASSWORD'],
            'Version': 2
        }
        self.proxies = {
            'http': app_config['HTTP_PROXY'],
            'https': app_config['HTTPS_PROXY']
        }


    def generate_xml_query(self, params):
        query = self.default_query.copy()
        query.update(params)
        return dicttoxml(
            {'Query':query},
            root=False,
            attr_type=False
        )

    def format_dmf_response(self, response, ssn):
        dmf_record = parker.data(fromstring(response.content))

        dmf_record_present = False
        full_name = None

        if dmf_record['Record'].get('DmfSearch', False):
            dmf_record_present = True

        if dmf_record['Record']['CommercialNameSearch'].get('Identity', False):
            full_name_string = dmf_record['Record']['CommercialNameSearch']['Identity']['NameInfo']['WholeName']
            full_name = full_name_string.split(',')[0]

        return {
            'ssn': ssn,
            'full_name': full_name,
            'dmf_record_present': dmf_record_present
        }

    def get_dmf_record(self, ssn):
        xml_query = self.generate_xml_query({
            'DmfSearch': 'yes',
            'Record': {
                'Ssn': ssn
            }
        })
        headers = {
        	"Content-Type": "text/xml",
        	"Content-Length": str(len(xml_query))
        }
        response = requests.post(
        	"https://secure.veris.net/cgi-bin/VerisNameSearchServer",
        	data=xml_query,
        	headers=headers,
            proxies=self.proxies
        )
        return self.format_dmf_response(response, ssn)
