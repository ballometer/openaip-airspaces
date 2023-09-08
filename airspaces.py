import json
import subprocess
import time
import glob

curl = 'curl -H "Host: stackoverflow.com" -H "Cache-Control: max-age=0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" -H "HTTPS: 1" -H "DNT: 1" -H "Referer: https://www.google.com/" -H "Accept-Language: en-US,en;q=0.8,en-GB;q=0.6,es;q=0.4" -H "If-Modified-Since: Thu, 23 Jul 2015 20:31:28 GMT" --compressed '

def get_all_features():
    all_features = []
    for filename in glob.glob('airspaces/*.geojson'):
        with open(filename) as f:
            data = json.load(f)
        all_features.extend(list(data['features']))

    return all_features

def download_schema():
    subprocess.run(curl + ' -o airspaces/schema.json https://www.flymap.org.za/openaip/geojsonbr/schema.json', shell=True)
    time.sleep(3)

# download_schema()

def get_limits(feature):
    levels = ['ll', 'ul']
    parts = {}
    for level in levels:
        value = feature['properties'][level]['value']
        unit = feature['properties'][level]['unit']
        referenceDatum = feature['properties'][level]['referenceDatum']

        if (unit, referenceDatum) == (0, 0):
            parts[level] = f'{value} m AGL'
        elif (unit, referenceDatum) == (0, 1):
            parts[level] = f'{value} m'
        elif (unit, referenceDatum) == (0, 2):
            parts[level] = f'{value} m STD'
        elif (unit, referenceDatum) == (1, 0):
            parts[level] = f'{value}AGL'
        elif (unit, referenceDatum) == (1, 1):
            parts[level] = f'{value}'
        elif (unit, referenceDatum) == (1, 2):
            parts[level] = f'{value} STD'
        elif (unit, referenceDatum) == (6, 0):
            parts[level] = f'FL{value}AGL'
        elif (unit, referenceDatum) == (6, 1):
            parts[level] = f'FL{value}'
        elif (unit, referenceDatum) == (6, 2):
            parts[level] = f'FL{value}'
        
        if value == 0 and referenceDatum == 0:
            parts[level] = 'GND'
    
    return f'{parts["ll"]}-{parts["ul"]}'
    
def get_schema():
    with open('airspaces/schema.json') as f:
        schema = json.load(f)
    return schema

schema = get_schema()

def get_short_type(feature, schema):
    t = feature['properties']['type']
    full_type = schema['type'][str(t)]
    if '(' in full_type:
        idx = full_type.find("(")
        short_type = full_type[idx+1:idx+4]
    else:
        short_type = full_type
    
    mappings = [
        ['Other', ''],
        ['Danger', 'D'],
        ['Restricted', 'R'],
        ['Prohibited', 'P'],
        ['Aerial Sporting Or Recreational Activity', '']
    ]

    for mapping in mappings:
        if short_type == mapping[0]:
            short_type = mapping[1]
    
    return short_type


all_features = get_all_features()

collection = {
    "type": "FeatureCollection",
    "features": []
}

for feature in all_features:
    limits = get_limits(feature)

    if feature['properties']['type'] == 0:
        if 'CTR' in feature['properties']['name']:
            feature['properties']['type'] = 4;
        if 'TMA' in feature['properties']['name']:
            feature['properties']['type'] = 7;

    short_type = get_short_type(feature, schema)
    if len(short_type) == 0 or len(short_type) > 3:
        short_description = limits
    else:
        short_description = f"{short_type} {limits}"

    description = feature['properties']['name']
    if 'freq' in feature['properties']:
        freq = feature['properties']['freq'][0]['val']
        if str(freq) not in description:
            description = f"{description} {freq}"
        del feature['properties']['freq']
    
    description = f"{description} {limits}"
    if short_type != '' and short_type not in description:
        description = f"{short_type} {description}"

    description = description.replace('   ', ' ')
    description = description.replace('  ', ' ')
    description = description.replace(' )', ')')
    description = description.replace(' ,', ',')

    short_description = short_description.replace('   ', ' ')

    del feature['properties']['ll']
    del feature['properties']['ul']
    del feature['properties']['_id']
    del feature['properties']['bnd']
    del feature['properties']['name']
    del feature['properties']['icao']
    

    feature['properties']['description'] = description
    # feature['properties']['short_description'] = short_description

    if feature['properties']['type'] in [0, 4, 7]:
        collection['features'].append(feature)

    # print(short_description)
    # print(description)
    # print()

with open('airspaces.json', 'w') as f:
    json.dump(collection, f)
