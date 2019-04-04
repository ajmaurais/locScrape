
import argparse
import pandas as pd

#my modules
import scraper

def getArgs():
    parser = argparse.ArgumentParser(description='Get ')

    parser.add_argument('-i', '--idCol', default = 'ID', type = str,
                        help = 'Name of column containing Uniprot IDs.')

    parser.add_argument('--nThread', default = None, type = int,
                        help = 'Number of threads to use to lookup uniprot anotations. '
                               'Default is the number of logical cores on your system.')

    parser.add_argument('ids', nargs='+')

    args = parser.parse_args()
    return args

def main():
    args = getArgs()

    locations = scraper.getLocList(args.ids, nThread = args.nThread)

    df = pd.DataFrame(data = {'ID': args.ids, 'location': locations})

    #for i, row in df.iterrows():
    #   row['location'] = scraper.getLocs(row['ID'])

    df.to_csv('../testFiles/temp.tsv', sep = '\t', index = False)

if __name__ == '__main__':
    main()
