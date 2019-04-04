# locScraper
Given a .tsv file with a column containing Uniprot protein IDs, scrape annotations for subcellular location from uniprot.org

## Installation
The simplest way to install `locScraper` is to download one of the precompiled binaries under the [releases](https://github.com/ajmaurais/locScraper/releases) tab. Binaries are available for OSX and CentOS.

You can also clone this repository with the command.
```
git clone https://github.com/ajmaurais/locScraper/tree/master
```

`locScraper` is written in `Python 3.7.1` If you elect to clone the repository, you must install `Python 3.7.1` and the flowing libraries:
```
pandas
tqdm
lxml
```

## Usage
```
usage: locScraper [-h] [-i IDCOL] [-l LOCCOL] [--nThread NTHREAD]
                  [-o OFNAME] [--inPlace]
                  input_file [input_file ...]

Get subcellular location annotations for a list of uniprot protein IDs.

positional arguments:
  input_file            .tsv or .csv files to process.

optional arguments:
  -h, --help            show this help message and exit

  -i IDCOL, --idCol IDCOL
                        Name of column containing Uniprot IDs.

  -l LOCCOL, --locCol LOCCOL
                        Name of new column to add with subcellular location.

  --nThread NTHREAD     Number of threads to use to lookup uniprot
                        annotations. Default is the number of logical cores on
                        your system.

  -o OFNAME, --ofname OFNAME
                        Name of output file. Default is <input_file>_loc.tsv.
                        If multiple input files are given, this argument is
                        ignored.

  --inPlace             Overwrite input files with output files. This option
                        overrides the --ofname option.
```
