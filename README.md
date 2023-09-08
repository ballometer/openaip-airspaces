# openaip-airspaces-pmtiles

Convert airspaces from [openAIP](https://openaip.net) to a pmtiles file.


## download and process airspaces

```bash
python3 download_airspaces.py
python3 airspaces.py
```

## convert .geojson to .pmtiles

```bash
git clone https://github.com/felt/tippecanoe.git
cd tippecanoe
make -j
```

```bash
tippecanoe/tippecanoe -o openaip-airspaces-2023-06-24.pmtiles airspaces.json -z 10 -Z 8 
```

You can find out the date stamp of the data at https://www.flymap.org.za/openaip/geojsonbr/lastUpdate.json
