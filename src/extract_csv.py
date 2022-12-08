import csv


# Extract the data from the CSV file and store it in a list
def extract_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        del[data[0]]
    # Map the data to a dictionary with the keys as the column names
    data_dict = {}
    for i in range(len(data)):
        data_dict[data[i][0]] = data[i][1:]
    return data_dict



# print(extract_csv('../data/Oreofe-Twitter2Scrape.csv'))
# print(extract_csv('../data/Oreofe-ScrapeDictionary.csv'))
