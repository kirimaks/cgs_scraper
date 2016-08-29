links = [
    'http://fairbanks.craigslist.org/res/5740880083.html',
    'http://fairbanks.craigslist.org/res/5740394184.html',
    'http://fairbanks.craigslist.org/res/5738031808.html',
    'http://fairbanks.craigslist.org/res/5732699010.html',
    'http://fairbanks.craigslist.org/res/5732643475.html',
    'http://fairbanks.craigslist.org/res/5725936371.html',
    'http://fairbanks.craigslist.org/res/5723208237.html',
    'http://fairbanks.craigslist.org/res/5722535708.html',
    'http://fairbanks.craigslist.org/res/5722299945.html',
    'http://fairbanks.craigslist.org/res/5713508096.html',
    'http://fairbanks.craigslist.org/res/5709186515.html',
    'http://fairbanks.craigslist.org/res/5704280001.html',
    'http://fairbanks.craigslist.org/res/5702461680.html',
    'http://fairbanks.craigslist.org/res/5694914428.html',
    'http://anchorage.craigslist.org/res/5740618166.html',
    'http://anchorage.craigslist.org/res/5764988229.html',
    'http://anchorage.craigslist.org/res/5764905098.html',
    'http://anchorage.craigslist.org/res/5750104070.html',
    'http://anchorage.craigslist.org/res/5748995201.html',
    'http://anchorage.craigslist.org/res/5748918627.html',
    'http://anchorage.craigslist.org/res/5758169690.html',
    'http://anchorage.craigslist.org/res/5758173676.html',
    'http://anchorage.craigslist.org/res/5758194235.html',
    'http://anchorage.craigslist.org/res/5758179862.html',
    'http://anchorage.craigslist.org/res/5764725326.html',
    'http://anchorage.craigslist.org/res/5764698990.html',
]

from subprocess import Popen, PIPE
import json
# from pprint import pprint
from multiprocessing import Pool


def start_casper(url):
    p = Popen(['casperjs', 'casper/parse_resume.js',
               '--url={}'.format(url)], stdout=PIPE)
    p.wait()
    resp = p.stdout.read().decode('utf-8')
    resp = json.loads(resp)
    return resp

results = list()

with Pool(processes=4) as pool:
    jobs = list()
    for link in links:
        jobs.append(pool.apply_async(start_casper, [link]))

    for job in jobs:
        results.append(job.get())

results = json.dumps(results)

with open("test.json", "w") as fl:
    fl.write(results)
