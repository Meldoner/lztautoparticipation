import json

cookies = [{}]
try:
    with open("cookies.txt", "r") as read_file:
        cookies = json.load(read_file)
except:
    pass

cookiecount = len(cookies)

cookienum = 0

try:
    for i in range(cookiecount):
        cookies[cookienum].pop('sameSite')
        cookienum = cookienum + 1
except:
    pass

