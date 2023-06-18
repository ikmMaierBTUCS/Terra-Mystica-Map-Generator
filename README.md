# Terra-Mystica-Map-Generator
Create a Terra Mystica map for a given river layout

Run the code in TM MapGen(1).py by executing the following commands:

1 Create a colorless map for given river layout with parameters (height, width, form, rivers)

you can also copy the layout of some well-known maps: original, F&I, fjords, loon lakes, archipelago and arrow

hex_map = HexagonalMap(height, width, form, rivers)

2 fill the map with colors

hex_map.create_map()

3 print the finished map as a string suitable for BGA format map-files

print(hex_map.bga_format())

4 print an ugly colored preview of the map

hex_map.display_final_map_colored()
