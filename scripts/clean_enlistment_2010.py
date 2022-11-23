import pandas as pd
import csv
from pprint import pprint

def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested "row" lists
    """
    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data


def write_csv(filepath, data, headers=None, encoding='utf-8', newline=''):
    """
    Writes data to a target CSV file. Column headers are written as the first
    row of the CSV file if optional headers are specified.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted
    fields may not be interpreted correctly by the csv.reader. On platforms that utilize
    `\r\n` an extra `\r` will be added.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list | tuple): sequence to be written to the target file
        headers (seq): optional header row list or tuple
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding, newline=newline) as file_obj:
        writer = csv.writer(file_obj)
        if headers:
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
        else:
            writer.writerows(data)

def fix_header(data):
    """
    Rename headers containing 'Total' to 'Total.' Function does not work.
    """
    for header in data:
        if 'total' in header.lower():
            header = 'Total'
    return data



def main():
    """
    Entry point for program. Controls workflow.

    Parameters:
        None
    Returns:
        None
    """

    # Load data
    df = pd.read_csv('../data/accession_zip_2010.csv')

    # Deal with merged cells and clean strings to ints
    df = df.ffill(axis = 1)
    df.replace(',','', regex=True, inplace=True)
    df = df.apply(pd.to_numeric, errors='ignore')

    # Split dataframe into headers and data
    df_headers = df.iloc[:4]
    df_data = df.iloc[4:]
    # print(df_data.dtypes)
    # print(df_headers.head())
    # print(df_data.head())
    # print(df_data.sample(n=5))

    # Write pandas dataframe to CSV and read in data from CSV
    df_data.to_csv('../data/enlist_data.csv')
    enlist_data_clean = read_csv('../data/enlist_data.csv')

    # Write pandas headers dataframe to CSV and read in data from CSV
    df_headers.to_csv('../data/enlist_headers.csv')
    enlist_headers = read_csv('../data/enlist_headers.csv')
    enlist_headers = enlist_headers[2:5]
    enlist_headers[0].insert(1, 'Index')
    enlist_headers[0].pop(0)
    enlist_headers[0][1] = enlist_headers[0][1].replace('1st 3 digits of ZIP CODE', '1st 3 digits')
    enlist_headers[1].pop(0)
    enlist_headers[2].pop(0)
    enlist_headers[1].insert(0, ' No.')
    enlist_headers[1].insert(1, '')
    enlist_headers[1].pop(1)
    enlist_headers[2].insert(1, ' Zip Code')

    # Merge data and headers and write to CSV
    combine = [i + j + z for i, j, z in zip(enlist_headers[0], enlist_headers[1], enlist_headers[2])]
    write_csv('../data/enlist_clean.csv', enlist_data_clean[1:], headers=combine, encoding='utf-8')
    enlist_fix = read_csv('../data/enlist_clean.csv')
    header_fix = enlist_fix[0]

    # Finder indexes for headers containing total
    for header in header_fix:
        if 'total' in header.lower():
            print(header_fix.index(header))

    # Rename headers with total; for some reason loop won't work
    header_fix[14] = 'Total'
    header_fix[17] = 'Total'
    header_fix[25] = 'Total'
    header_fix[31] = 'Total'
    header_fix[44] = 'Total'
    header_fix[47] = 'Total'
    header_fix[55] = 'Total'
    header_fix[60] = 'Total'

    # Write to CSV
    write_csv('../data/enlist_clean.csv', enlist_data_clean[1:], headers=header_fix, encoding='utf-8')

if __name__ == "__main__":
    main()