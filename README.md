# locScraper
Given a .tsv file with a column containing Uniprot protein IDs, scrape annotations for subcellular location from Uniprot.org

## Installation
The simplest way to install `locScraper` is to download one of the precompiled binaries under the [releases](https://github.com/ajmaurais/locScraper) tab. Binaries are available for OSX and CentOS. 

You can also clone this repository with the command.
```
git clone https://github.com/ajmaurais/locScraper
```

`locScraper` is written in `Python 3.7` If you elect to clone the repository, you must install `Python 3.7` and the flowing libraries:
```
tqdm
lxml
```

## Usage
```
usage: locScraper [-h] [-i IDCOL] [--columns {sl,go,all}] [--locCol LOCCOL]
                  [--goCol GOCOL] [--allCol ALLCOL] [--nThread NTHREAD]
                  [-o OFNAME] [--inPlace]
                  input_file [input_file ...]

Get subcellular location annotations for a list of Uniprot protein IDs. A
column in input_file should contain Uniprot IDs. After locScraper runs,
columns will be added for Unipriot location annotations, GO cellular component
annotations.

positional arguments:
  input_file            .tsv or .csv files to process.

optional arguments:
  -h, --help            show this help message and exit

  -i IDCOL, --idCol IDCOL
                        Name of column containing Uniprot IDs.

  --columns {sl,go,all}
                        Which new columns should be added?
                        sl : Uniprot annotation for subcellular location
                        go : GO annotation for cellular component
                        all : both sl and go
                        Default is all.

  --locCol LOCCOL       Name of new column to add with subcellular location.

  --goCol GOCOL         Name of new column to add with GO cellular component
                        annotation.

  --allCol ALLCOL       Name of new column to add with GO and Uniprot
                        annotations combined.

  --nThread NTHREAD     Number of threads to use to lookup Uniprot
                        annotations. Default is the number of logical cores on
                        your system.

  -o OFNAME, --ofname OFNAME
                        Name of output file. Default is <input_file>_loc.tsv.
                        If multiple input files are given, this argument is
                        ignored.

  --inPlace             Overwrite input files with output files. This option
                        overrides the --ofname option.
```
