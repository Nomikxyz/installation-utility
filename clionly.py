# Import csv
import csv
# Import os
import os

# Main Function
def main():
    # Open dataset file
    dataset = open('dataset.csv')

    # Initialize csvreader for dataset
    reader = csv.reader(dataset)

    # Read data from reader
    data = list(reader)

    # Variables for progress counter
    lines = len(data)
    i = 0

    # Analyze data in dataset
    for row in data:
        # Assign image name and state to variables
        package = row[0]

        # Increment i
        i += 1

        os.system("cpanm "+package)

# Execute main function if name is equal to main
if __name__ == '__main__':
    main()