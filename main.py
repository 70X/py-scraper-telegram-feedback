from crawler import Crawler
from push_notifications import PushNotifications
import constants
import schedule
import time
import datetime

crawler = Crawler()
push = PushNotifications(constants.debug)

def processPage(url, sizes, notificationUsers, colors):
  crawler.setUrl(url)
  crawler.readPage()
  for size in sizes:
    results = crawler.checkAvailability(size, colors)
    for data in results:
      push.sendMessage(notificationUsers, "url: {}\nsize: {}\ndata: {}".format(url, size, data))

def job():
  for data in constants.pageUrls:
    processPage(data['url'], data['sizes'], data['notificationUsers'], data.get('colors'))

# job()
push.sendMessageToMe([], 'Bike Decathlon Script has just started with {} urls'.format(len(constants.pageUrls)))

schedule.every(1).hours.do(lambda: push.sendMessageToMe([], 'Still running...'))
schedule.every(30).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)