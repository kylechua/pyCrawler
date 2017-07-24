
# Database of API URLs, parser names
class db:
    # 'name':'defaultAPIurl'
    api = {
        'xiaozhu':'http://www.xiaozhu.com/ajax.php?op=Ajax_GetDatas4Map&partner=&startDate=&endDate=&city=&putkey=&district=&landmark=&housetyperoomcnt=&facilities=&leasetype=&guestnum=&lowprice=&highprice=&pageno=&sort=&_='
    }
    # 'name':'package.module_name'
    parser = {
        'default':'package.parser_default',
        'xiaozhu':'package.parser_xiaozhu'
    }

###
###
###

def getapiURL(source):
    if source in db.api:
        return db.api[source]
    else:
        return source

def getparser(source):
    if source in db.parser:
        return db.parser[source]
    else:
        return db.parser['default']

# Colors for console messages
# Source: https://stackoverflow.com/a/287944
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'