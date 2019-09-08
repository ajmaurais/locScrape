
import argparse
import sys

#my modules
import scraper
import dataframe
import base_parser

def getArgs():
    parser = argparse.ArgumentParser(prog = 'scrape_keywords',
                                     description='Get CV terms and values from the "Keywords" table for a list of '
                                                 'Uniprot protein IDs. A column in input_file should contain Uniprot '
                                                 'IDs. After scrape_keywords finishes, columns will be added for each '
                                                 'CV term and value.',
                                     parents=[base_parser.parent_parser])

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

        headers = set()
        for f in functions:
            headers.update(f.keys())

        print_headers = [h.replace(' ', '_').lower() for h in headers]

        #add columns to df
        sys.stdout.write('Adding columns:\n')
        for k, h in zip(headers, print_headers):
            sys.stdout.write('\t{}\n'.format(h))
            df[h] = [f[k] if k in f else '' for f in functions]

        #write results
        df.to_csv(ofnames[i], sep = '\t')
        sys.stdout.write('Results written to {}\n\n'.format(ofnames[i]))


if __name__ == '__main__':
    main()
