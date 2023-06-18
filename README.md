# Terra-Mystica-Map-Generator
Create a Terra Mystica map for a given river layout

Run the code by executing the following commands:

1 Create a colorless map for given river layout with parameters (height, width, form, rivers)

you can also copy the layout of some well-known maps: original, F&I, fjords, loon lakes, archipelago and arrow

hex_map = HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)])

2 fill the map with colors

hex_map.create_map()

3 print the finished map as a string suitable for BGA format map-files

print(hex_map.bga_format())

4 print an ugly colored preview of the map

hex_map.display_final_map_colored()
