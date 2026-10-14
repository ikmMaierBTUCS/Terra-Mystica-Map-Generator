# Terra-Mystica-Map-Generator

Generates balanced maps for the board game Terra Mystica for a given river layout.
The generated maps are played on [Board Game Arena](https://boardgamearena.com) and can be created in the web app https://tm-mapgen.ikmaier.workers.dev/.

![Examples of generated maps](Examples%20of%20generated%20maps.png)

## How it works
The map is coloured hex by hex. The probability of a hex becoming green (or another colour) is the higher, the farther away the next green hex is - based on a measure of how many ships/spades are required to reach it.
Each colour also keeps track of its luck, i.e. how much more valuable hexes near the center of the map it got than it could expect.
A finished map is only accepted if all colours have about the same number of hexes, the same river access and the same luck. Otherwise the map is coloured again.

## Download maps for Board Game Arena
Just download from `TMMapGen24-01 maps.zip` one of the files map3XX.txt.
We have various different river layouts: map300-map305 = base map layout; -311 = fjords; -317 = fire&ice; -323 = loonlakes; -329 = arrow; -335 = archipelago; -341 = onion; -347 = 7isles; -353 = heart; -359 = peninsulas; -365 = twisty-land; -371 = ai1; -377 = ai2; -382 = bend; -387 = big-river; -391 = pirates-bay; -395 = swamp; -399 = central-island

## Generate maps yourself
```
pip install -r requirements.txt
python tm_mapgen.py fjords
```
This prints a fjords map in BGA format and shows a coloured preview of it. Run `python tm_mapgen.py -h` to see all river layouts and options, e.g.
```
python tm_mapgen.py fjords -n 6 --save 306
```
generates 6 maps and saves them as map306.txt, ..., map311.txt.

You can also use the code in Python with your own river layout:
```python
from tm_mapgen import HexagonalMap, create_balanced_map, plot_map

# 1 create a colorless map for a given river layout with parameters (height, width, form, rivers, start)
hex_map = HexagonalMap(9, 13, 0, [(1,1), (2,1), (5,1), ...])

# 2 fill the map with colors
hex_map, statistics = create_balanced_map(hex_map)

# 3 print the finished map as a string suitable for BGA format map-files
print(hex_map.bga_format())

# 4 show a colored preview of the map
plot_map(hex_map)
```
The parameters are explained in `HexagonalMap.__init__`. You can also copy one of the river layouts in `LAYOUTS`.

## Versions
The map generator has been improved in several versions, see the [releases](https://github.com/ikmMaierBTUCS/Terra-Mystica-Map-Generator/tags). Version 4 is used on Board Game Arena.
