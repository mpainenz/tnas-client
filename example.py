from connection import api_client

username = 'something'
password = '12345678920'
carrier_id = '12356'

tnas_connection = api_client.TNASConnection(api_client.TNAS_TEST)
tnas_connection.login(username=username, password=password, carrier_id=carrier_id)
