
#base uniprot url
UNIPROT_URL = 'http://www.uniprot.org/uniprot/'

#page error message
REQUEST_ERROR = 'error_getting_page'
UNIPROT_ERROR = 'no_uniprot_records_found'


#subcelluar location xpaths
SL_XPATH = '//*[@id="table-uniprot_annotation"]/div/ul/li/h6/text()'
SSL_XPATH = '//*[@id="table-uniprot_annotation"]/div/ul/li/ul/li/a/text()'

#go celluar component xpaths
GO_XPATH = '//*[@id="table-go_annotation"]/div/ul/li/h6/text()'
SGO_XPATH = '//*[@id="table-go_annotation"]/div/ul/li/ul/li/a/text()'

#paths for molecular function and ligand keywords
FXN_PATH = "//*[@class = 'databaseTable']//tr[1]/td/span/a[starts-with(@href, '/keywords/')]/text()"
LIGAND_PATH = "//*[@class = 'databaseTable']//tr[2]/td/span/a[starts-with(@href, '/keywords/')]/text()"