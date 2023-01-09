
import re

#base uniprot url
UNIPROT_URL = 'https://rest.uniprot.org/uniprotkb/'

#page error message
REQUEST_ERROR = 'error_getting_page'
UNIPROT_ERROR = 'no_uniprot_records_found'
ERROR_HEADER = 'ERROR'

# subcelluar location xpaths
SL_XPATH = '//comment[@type="subcellular location"]/subcellularlocation/location/text()'

# GO term xpath
GO_XPATH = '//dbreference[@type="GO"]/property[@type="term"]/@value'

#paths for molecular function and ligand keywords
KEYWORD_XPATH = ''

# GO term patterns
CELLULAR_COMPONENT_RE = re.compile('^C:')

