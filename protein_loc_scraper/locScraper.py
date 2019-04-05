
import argparse
import os
import sys

#my modules
import scraper
import dataframe

def getArgs():
    parser = argparse.ArgumentParser(prog = 'locScraper',
                                     description='Get subcellular location annotations for a list of Uniprot protein IDs. '
                                                 'A column in input_file should contain Uniprot IDs. After locScraper '
                                                 'runs, columns will be added for Unipriot location annotations, '
                                                 'GO celluar component annotations.')

    parser.add_argument('-i', '--idCol', default = 'ID', type = str,
                        help = 'Name of column containing Uniprot IDs.')

    parser.add_argument('--columns', choices= ['sl', 'go', 'all'], default =  'all',
                        help = 'Which new columns should be added? Default is all.')

    parser.add_argument('--locCol', default='subcellular_loc',
                        help='Name of new column to add with subcellular location.')

    parser.add_argument('--goCol', default='go_cellular_component',
                        help='Name of new column to add with GO cellular component annotation.')

    parser.add_argument('--allCol', default='all_locations',
                        help='Name of new column to add with GO and Uniprot annotations combined.')

    parser.add_argument('--nThread', default = None, type = int,
                        help = 'Number of threads to use to lookup Uniprot annotations. '
                               'Default is the number of logical cores on your system.')

    parser.add_argument('-o', '--ofname', type = str, default = None,
                        help = 'Name of output file. Default is <input_file>_loc.tsv. '
                               'If multiple input files are given, this argument is ignored.')

    parser.add_argument('--inPlace', default = False, action = 'store_true',
                        help = 'Overwrite input files with output files. '
                               'This option overrides the --ofname option.')

    parser.add_argument('input_file', nargs='+',
                        help = '.tsv or .csv files to process.')

    args = parser.parse_args()

    #manually processing of certian args
    ofnames = list()
    if args.inPlace:
        ofnames = args.input_file
    else:
        for fname in args.input_file:
            ofnames.append('{}_loc.tsv'.format(os.path.splitext(fname)[0]))
        if args.ofname is not None and len(args.input_file) > 1:
            ofnames = [args.ofname]

    return args, ofnames


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
        locations = scraper.getLocList(ids, nThread = args.nThread)

        #transpose locations so columns can easily be added to df
        locations = list(zip(*locations))

        #add columns to df
        if args.columns == 'all' or args.columns == 'sl':
            df[args.locCol] = locations[0]
        if args.columns == 'all' or args.columns == 'go':
            df[args.goCol] = locations[1]
        if args.columns == 'all':
            df[args.allCol] = locations[2]

        #write results
        df.to_csv(ofnames[i], sep = '\t')
        sys.stdout.write('Results written to {}\n\n'.format(ofnames[i]))


if __name__ == '__main__':
    main()
