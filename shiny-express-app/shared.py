# shared.py

# contents run once per startup, whereas 
# contents in app.py run once per session

from pathlib import Path
import pyarrow.feather as feather

bikes = feather.read_feather(Path(__file__).parent.parent / "data/bikes_info.arrow")
stations = feather.read_feather(Path(__file__).parent.parent / "data/stations_info.arrow")
