import urllib3
import certifi
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())
response = http.request(
    "GET",
    "https://www.google.co.th",
)
print(response.status)