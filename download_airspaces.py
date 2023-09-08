import json
import subprocess
import time

curl = 'curl -H "Host: stackoverflow.com" -H "Cache-Control: max-age=0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" -H "HTTPS: 1" -H "DNT: 1" -H "Referer: https://www.google.com/" -H "Accept-Language: en-US,en;q=0.8,en-GB;q=0.6,es;q=0.4" -H "If-Modified-Since: Thu, 23 Jul 2015 20:31:28 GMT" --compressed '

def download_countries():
    subprocess.run(curl + ' -o airspaces/countries.json https://www.flymap.org.za/openaip/geojsonbr/countries.json', shell=True)
    time.sleep(3)
    with open('airspaces/countries.json') as f:
        countries = json.load(f)

    for country in countries:
        print('download ' + country['name'] + '...')
        subprocess.run(curl + f' -o airspaces/{country["name"]}.geojson https://www.flymap.org.za/openaip/geojsonbr/{country["name"]}.geojson', shell=True)
        time.sleep(3)

download_countries()
