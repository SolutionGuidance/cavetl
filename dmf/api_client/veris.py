from .client import SsnApiClient
from dicttoxml import dicttoxml
from xml.etree.ElementTree import fromstring
from xmljson import parker
import pdb
import requests

class VerisSsnClient(SsnApiClient):
    def __init__(self, user_id=None, password=None, http_proxy=None, https_proxy=None):
        self.default_query = {
            'UserID': user_id,
            'Password': password,
            'Version': 2
        }
        self.proxies = {
            'http': http_proxy,
            'https': https_proxy
        }


    def generate_xml(self, query):
        return dicttoxml(
            query,
            root=False,
            attr_type=False
        )

    def getDmfRecord(self, ssn):
        query = self.default_query.copy()
        query.update({
            'DmfSearch': 'yes',
            'Record': {
                'Ssn': ssn
            }
        })
        xml = self.generate_xml({'Query':query})
        headers = {
        	"Content-Type": "text/xml",
        	"Content-Length": str(len(xml))
        }
        response = requests.post(
        	"https://secure.veris.net/cgi-bin/VerisNameSearchServer",
        	data=xml,
        	headers=headers,
            proxies=self.proxies
        )
        return parker.data(fromstring(response.content))

    #def getDmfRecord(self, ssn):
    #    return self.dmfRecordQuery(ssn)
