import os

# all bingo versions and their start dates (ordered from new to old)
VERSIONS = {
    'v9.3' : '09-06-2018',
    'v9.2' : '08-10-2016',
    'v9.1' : '02-07-2016',
    'v9'   : '09-04-2016',
    'v8.5' : '30-01-2016',
    'v8.4' : '13-12-2014',
    'v8.3' : '13-09-2014',
    'v?'   : '01-06-2011',
    'v2'   : '01-01-1990'
}

def get_newest_version():
    return list(VERSIONS.keys())[0]

def is_supported_version(version):
    return os.path.isfile('BingoBoards/Versions/' + version.replace('.','') + '.bingo')

# race IDs that should be ignored (for various reasons)
BLACKLIST = [
    '219509', # scara's wr Kappa

    # blackouts:
    '100176',
    '67638',
    '91357',
    '86393',
    '108069',
    '90718',
    '128327',
    '176483',

    # double:
    '18042',
    '17667',
    '18680',
    '15910',
]