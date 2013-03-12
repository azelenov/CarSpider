import requests
from settings import ref_urls

def check_rest():
    url = ref_urls['dev']
    r = requests.get(url)
    print r.status_code
    print r.content

check_rest()

