from more_itertools import unique_everseen

with open('barcodes.csv', 'r') as f, open('barcodes_RemoveDupe.csv', 'w') as out_file:
    out_file.writelines(unique_everseen(f))