
#base uniprot url
UNIPROT_URL = 'http://www.uniprot.org/uniprot/'

#page error message
REQUEST_ERROR = 'error_getting_page'
UNIPROT_ERROR = 'no_uniprot_records_found'
ERROR_HEADER = 'ERROR'

#subcelluar location xpaths
SL_XPATH = '//*[@id="table-uniprot_annotation"]/div/ul/li/h6/text()'
SSL_XPATH = '//*[@id="table-uniprot_annotation"]/div/ul/li/ul/li/a/text()'

#go celluar component xpaths
GO_XPATH = '//*[@id="table-go_annotation"]/div/ul/li/h6/text()'
SGO_XPATH = '//*[@id="table-go_annotation"]/div/ul/li/ul/li/a/text()'

#paths for molecular function and ligand keywords
BASE_KEYWORD_DAT_PATH = "//*[@class = 'databaseTable']//tr[{}]/td/span/a[starts-with(@href, '/keywords/')]/text()"
KEYWORD_HEADER_PATH = "//*[@class = 'databaseTable']//tr/td[1]/text()"
