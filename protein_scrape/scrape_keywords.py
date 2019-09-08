
import argparse
import sys

#my modules
import scraper
import dataframe

import base_parser

def getArgs():
    parser = argparse.ArgumentParser(prog = 'scrape_loc',
                                     description='Get subcellular location annotations for a list of Uniprot protein IDs. '
                                                 'A column in input_file should contain Uniprot IDs. After locScrape '
                                                 'finishes, columns will be added for Unipriot location annotations, '
                                                 'GO celluar component annotations.',
                                     parents=[base_parser.parent_parser])

    parser.add_argument('--columns', choices= ['fxn', 'ligand', 'all'], default =  'all',
                        help = 'Which new columns should be added? Default is all.')

    parser.add_argument('--fxnCol', default='molecular_function',
                        help='Name of new column to add with molecular function.')

    parser.add_argument('--ligandCol', default='ligand',
                        help='Name of new column to add with ligand annotation.')

    parser.add_argument('--allCol', default='all_locations',
                        help='Name of new column to add with GO and Uniprot annotations combined.')

    args = parser.parse_args()

    return args, base_parser.process_ofnames(args, 'fxn')


def main():
    args, ofnames = getArgs()

    for i, ifname in enumerate(args.input_file):
        sys.stdout.write('Working on {}...\n'.format(ifname))
        df = dataframe.read_tsv(ifname)

        #get list of Uniprot IDs
        sys.stdout.write('Using \'{}\' as the Uniprot ID column.\n'.format(args.idCol))
        try:
            ids = df[args.idCol]
        except KeyError as e:
            sys.stderr.write('Error in {}: {}\nSkipping...\n'.format(ifname, e))
            continue

        #get locations
        functions = scraper.getFxnList(ids, nThread = args.nThread)
        #
        #transpose functions so columns can easily be added to df
        functions = list(zip(*functions))

        #add columns to df
        if args.columns == 'all' or args.columns == 'fxn':
            df[args.fxnCol] = functions[0]
        if args.columns == 'all' or args.columns == 'ligand':
            df[args.ligandCol] = functions[1]
        if args.columns == 'all':
            df[args.allCol] = functions[2]

        #write results
        df.to_csv(ofnames[i], sep = '\t')
        sys.stdout.write('Results written to {}\n\n'.format(ofnames[i]))


if __name__ == '__main__':
    main()
