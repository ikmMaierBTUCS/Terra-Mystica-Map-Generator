# Terra-Mystica-Map-Generator

Here, you can download randomly generated maps to use for playing on BoardGameArena.

Just download one of the files map3XX.txt from TMMapGen24-01 maps.zip. 
We have various different river layouts: map300-map305 = base map layout; -311 = fjords; -317 = fire&ice; -323 = loonlakes; -329 = arrow; -335 = archipelago; -341 = onion; -347 = 7isles; -353 = heart; -359 = peninsulas; -365 = twisty-land; -371 = ai1; -377 = ai2; -382 = bend; -387 = big-river; 391 = pirates-bay; -395 = swamp; -399 = central-island

Or, use the code to...

Create a Terra Mystica map for a given river layout

Run the code in TM MapGen(1).py by executing the following commands:

1 Create a colorless map for given river layout with parameters (height, width, form, rivers, start)

you can also copy the layout of some well-known maps: original, F&I, fjords, loon lakes, archipelago and arrow

hex_map = HexagonalMap(height, width, form, rivers)

2 fill the map with colors

hex_map.create_map()

3 print the finished map as a string suitable for BGA format map-files

print(hex_map.bga_format())

4 print an ugly colored preview of the map

hex_map.display_final_map_colored()
