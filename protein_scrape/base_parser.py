
import argparse
import os

ID_COL = 'ID'

def process_ofnames(args, post):
    # manually process of some args
    ofnames = list()
    if args.inPlace:
        ofnames = args.input_file
    else:
        for fname in args.input_file:
            ofnames.append('{}_{}.tsv'.format(os.path.splitext(fname)[0], post))
        if args.ofname is not None and len(args.input_file) > 1:
            ofnames = [args.ofname]
    return ofnames


parent_parser = argparse.ArgumentParser(add_help=False)

parent_parser.add_argument('-i', '--idCol', default = ID_COL, type = str,
                           help = 'Name of column containing Uniprot IDs. '
                                  'Default is "{}".'.format(ID_COL))

parent_parser.add_argument('--nThread', default=None, type=int,
                           help='Number of threads to use to lookup Uniprot annotations. '
                                'Default is the number of logical cores on your system.')

parent_parser.add_argument('--verbose', default=False, action='store_true',
                           help='If set, verbose output will be printed when --hThread is 1.')

parent_parser.add_argument('-o', '--ofname', type=str, default=None,
                           help='Name of output file. Default is <input_file>_loc.tsv. '
                                'If multiple input files are given, this argument is ignored.')

parent_parser.add_argument('--inPlace', default=False, action='store_true',
                           help='Overwrite input files with output files. '
                                'This option overrides the --ofname option.')

parent_parser.add_argument('input_file', nargs='+',
                    help='.tsv or .csv files to process.')
