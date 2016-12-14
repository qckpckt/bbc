import csv


def export_to_csv(list_of_dicts, name_of_file):
    '''
    Exports a list of dictionaries to a csv.

    @param list_of_dicts a list of dictionaries.
    @param name_of_file the name of the file to export to.
    '''

    with open(name_of_file, 'w') as csvfile:
        fieldnames = list(list_of_dicts[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in list_of_dicts:
            writer.writerow(record)
