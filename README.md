# Terra-Mystica-Map-Generator
Create a Terra Mystica map for a given river layout

# Run the code by executing the following commands:

#1 Create a colorless map for given river layout with parameters (height, width, form, rivers)
# height is the number of horizontal lines of hexes
# width is the number of hexes in in the LONGER lines (remember that between 2 longer lines is a line shorter by one)
# form = 0, if the uppermost line is longer, form = 1, if the uppermost line is shorter
# rivers is the list of coordinates occupied by rivers. CAUTION: the coordinates are written (column, row)
# here you can copy the layout of some well-known maps:
#archipelago: HexagonalMap(9,13,0,[(6,0),(10,0),(6,1),(7,1),(9,1),(6,2),(8,2),(9,2),(10,2),(11,2),(0,3),(4,3),(5,3),(3,3),(8,3),(11,3),(1,4),(3,4),(5,4),(6,4),(9,4),(1,5),(2,5),(5,5),(6,5),(7,5),(8,5),(11,5),(6,6),(9,6),(10,6),(11,6),(6,7),(8,7),(6,8),(9,8)])
#onion: HexagonalMap(9,13,0,[(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(2,2),(3,2),(9,2),(10,2),(2,3),(6,3),(9,3),(3,4),(5,4),(6,4),(7,4),(9,4),(10,4),(11,4),(12,4),(1,5),(2,5),(6,5),(10,5),(2,6),(3,6),(4,6),(9,6),(10,6),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7)])
#loon: HexagonalMap(9,13,1,[(8,0),(9,0),(3,1),(4,1),(7,1),(10,1),(1,2),(2,2),(6,2),(10,2),(3,3),(7,3),(8,3),(10,3),(2,4),(5,4),(6,4),(8,4),(1,5),(4,5),(6,5),(8,5),(1,6),(2,6),(3,6),(9,6),(10,6),(3,7),(7,7),(8,7),(11,7),(2,8),(4,8),(5,8),(6,8)])
#FI: HexagonalMap(9,13,1,[(1,0),(5,0),(2,1),(6,1),(7,1),(8,1),(2,2),(3,2),(4,2),(8,2),(9,2),(10,2),(11,2),(12,2),(5,3),(9,3),(0,4),(1,4),(3,4),(4,4),(9,4),(2,5),(3,5),(5,5),(6,5),(7,5),(10,5),(1,6),(7,6),(10,6),(2,7),(7,7),(10,7),(2,8),(7,8),(10,8)])
#fjords: HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)])
#original: HexagonalMap(9,13,0,[(1,1),(2,1),(5,1),(6,1),(9,1),(10,1),(0,2),(1,2),(3,2),(5,2),(7,2),(9,2),(11,2),(12,2),(3,3),(4,3),(7,3),(9,3),(8,4),(9,4),(2,5),(3,5),(6,5),(7,5),(8,5),(0,6),(1,6),(2,6),(4,6),(6,6),(8,6),(3,7),(4,7),(5,7),(8,7),(9,8)])

hex_map = HexagonalMap(9,13,0,[(2,0),(2,1),(6,1),(7,1),(8,1),(9,1),(10,1),(3,2),(4,2),(6,2),(11,2),(0,3),(1,3),(2,3),(4,3),(5,3),(11,3),(12,3),(3,4),(6,4),(11,4),(2,5),(6,5),(10,5),(2,6),(7,6),(10,6),(1,7),(7,7),(8,7),(9,7),(1,8),(2,8),(7,8)])

#2 fill the map with colors
hex_map.create_map()

#3 print the finished map as a string suitable for BGA format map-files
print(hex_map.bga_format())

#4 print an ugly colored preview of the map
hex_map.display_final_map_colored()
