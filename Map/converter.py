import sys
import csv

# Convert CSV to pg.Vector2
# Usage
# Location: ./Map
# Command: $ py converter.py <csv_file_name> <map_name>
# e.g. $py converter.py map_1 map_1

def main(file_name: str, output_name: str):
    sys.stdout = open(F"{output_name}.py", 'w')
    sys.stdout.write("import pygame as pg\n\n")
    
    with open(F"CSV\{file_name}.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rows = list(reader)

        # OBSTACLE
        sys.stdout.write("OBSTACLE_POSITION = [")
        first_in_file = True
        counter = 0
        x, y = 0.5, 0.5
        for row in rows:
            x = 0.5
            for val in row:
                if val == '1':
                    if not first_in_file:
                        sys.stdout.write(", ")
                    if counter % 4 == 0:
                        sys.stdout.write(" \\\n\t")
                    sys.stdout.write(F"pg.Vector2({x},{y})")
                    first_in_file = False
                    counter += 1
                x += 1
            y += 1
        sys.stdout.write("]\n")

        # RE FIELD
        sys.stdout.write("RE_FIELD_POSITION = [")
        first_in_file = True
        counter = 0
        x, y = 0.5, 0.5
        for row in rows:
            x = 0.5
            for val in row:
                if val == '2':
                    if not first_in_file:
                        sys.stdout.write(", ")
                    if counter % 4 == 0:
                        sys.stdout.write(" \\\n\t")
                    sys.stdout.write(F"pg.Vector2({x},{y})")
                    first_in_file = False
                    counter += 1
                x += 1
            y += 1
        sys.stdout.write("]\n")
    
    sys.stdout.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])