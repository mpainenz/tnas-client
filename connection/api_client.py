import urllib, ssl
from urllib import request
import xml.etree.ElementTree as ET

TNAS_LIVE = "LIVE"
TNAS_TEST = "TEST"


class TNASConnection:

    def __init__(self, tnas_interface):
        assert tnas_interface in [TNAS_LIVE, TNAS_TEST]
        print("TNAS API Connecting to {} TNAS Interface".format(tnas_interface))

        self.tnas_interface = tnas_interface
        self.ssl_processor = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
        self.cookie_processor = urllib.request.HTTPCookieProcessor()
        self.http_opener = urllib.request.build_opener(self.cookie_processor, self.ssl_processor)

    def login(self, username, password, carrier_id):
        print("Performing Login")
        print("Username: {}".format(username))
        print("Password: ********")
        print("Carrier ID: {}".format(carrier_id))
        params = [username, password, None, carrier_id]
        request_xml = self.generate_request_xml(tnas_method_name='login', params=params)
        response_xml = self.perform_http_request(request_xml)
        response_data = self.parse_response_xml(response_xml)

        if response_data['resultCode'] == 0:
            print("Connected to TNAS {}, Session ID: {}".format(response_data['systemId'], response_data['sessionId']))
        else:
            print("Error Connecting to TNAS, Result Code: {}".format(response_data['resultCode']))

    def generate_request_xml(self, tnas_method_name, params):
        # Constructs a function call into the XML format required by TNAS
        xml = '<?xml version="1.0" encoding="ISO-8859-1"?>' \
              + '<methodCall>' \
              + '<methodName>' \
              + 'Tnas._{}'.format(tnas_method_name) \
              + '</methodName>' \
              + '<params>'

        for param in params:
            if param is None:
                param_str = '&lt;NULL>'
            else:
                param_str = param
            xml = xml + '<param>' \
                  + '<value>' \
                  + param_str \
                  + '</value>' \
                  + '</param>'

        xml = xml + '</params>' \
              + '</methodCall>'
        return xml

    def perform_http_request(self, xml_request):
        # Perform an HTTP Post against TNAS and return the raw HTTP Response Data
        url = 'https://ipms-{}.tcf.org.nz:8143/tnas/interface'.format(self.tnas_interface)
        http_request = request.Request(url, xml_request.encode("utf-8"))
        http_request.get_method = lambda: "POST"
        page = self.http_opener.open(http_request)
        return page.read()

    def parse_response_xml(self, response_xml):
        # Convert an XML response into a more usable Python Dict

        # Parses the response_xml into a Python XML Element Tree object
        root_node = ET.fromstring(response_xml)

        # Get the first '<member>' node
        member_node = root_node[0][0][0][0][0]

        # Get the Struct of the result
        result_struct_node = member_node[1][0]

        response_dict = {}

        for result_item in result_struct_node:
            member_name = result_item.find('name')
            member_value = result_item.find('value')

            if member_value.text is not None:
                response_dict[member_name.text] = member_value.text
            else:
                int_value = member_value.find('int')
                if int_value is not None:
                    response_dict[member_name.text] = int(int_value.text)

        return response_dict

