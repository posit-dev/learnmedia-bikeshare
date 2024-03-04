# Bikeshare Data


We collected the bikeshare data from the public APIs provided by three
cities:

- Austin, TX - https://gbfs.bcycle.com/bcycle_austin/gbfs.json
- Chicago, IL - https://gbfs.divvybikes.com/gbfs/2.3/gbfs.json
- Washington, DC - https://gbfs.capitalbikeshare.com/gbfs/gbfs.json

## Data

We then used Posit Connect’s [scheduling
features](https://docs.posit.co/connect/user/scheduling/index.html) to
update the pins at regular intervals.

To download the `pin`ned data, click below. The data is available in
four different formats:

- [csv](https://colorado.posit.co/rsc/content/5c1c26ca-1e8d-4885-a890-fadc625d96dd/stations_csv.csv)
- [Arrow](https://colorado.posit.co/rsc/content/1e885c13-1d6e-470f-b7e4-af3fa5ba3119/stations_arrow.arrow)
- [Parquet](https://colorado.posit.co/rsc/content/11b76cda-4d2a-43d9-a3af-6be55620cb69/stations_parquet.parquet)

This repository also contains two helpful local files:

- [data/stations_info.arrow](stations_info.arrow) the locations and
  names of bikeshare stations within the three cities.
- [data/bikes_info.arrow](bikes_info.arrow) contains a truncated,
  local version of the pinned data to use in the template apps.
