import requests
import json
from calendar import monthrange
from ast import literal_eval


years=['2018','2017','2016','2015','2014','2013','2012','2011']

months=['01','02','03','04','05','06','07','08','09','10','11','12']


def dateformater(years,months):
    total_size = 0
    url_errors=[]
    for year in years:
        for month in months:
            (first,last) = monthrange(int(year),int(month))
            days = ranges(last,10)
            for day in days:
                (f,l) = literal_eval(day)
                after=year+"-"+month+"-"+"{0:0=2d}".format(f)
                before=year+"-"+month+"-"+"{0:0=2d}".format(l)
                url = "https://api.pushshift.io/reddit/comment/search/?subreddit=portugal&size=500&after="+after+"&before="+before
                data = requests.get(url)
                print(url)
                total_size += len(data.content)
                file_name = "./data/data("+after+"_"+before+").json"
                with open(file_name, "a+") as d:
                    try:
                        json.dump(json.loads(data.content.decode("utf-8")), d)
                        d.close()
                    except:
                        url_errors.append(url)
                        print("=>erro no url: "+url)
    return total_size,url_errors

def ranges(N, nb):
    step = N / nb
    return ["({},{})".format(round(step*i)+1, round(step*(i+1))) for i in range(nb)]

t_size, errors_list = dateformater(years,months)
with open("errors.txt", "a+") as f:
    for u in errors_list:
        f.write(u)

print(t_size)
