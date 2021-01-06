import requests
from bs4 import BeautifulSoup


class Crawler:
    url = None
    page = None
    soup = None

    def __init__(self):
        pass

    def setUrl(self, url):
        self.url = url

    def readPage(self):
        if self.url is None:
            raise Exception("Sorry, url is not set")
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.page = page.content
        self.soup = soup

    def getModelColors(self, colors):
        results = []
        colorsNode = self.soup.findAll("div", {"class": "model-selection"})
        for node in colorsNode:
            colorId = node.attrs['data-model-id']
            color = node.attrs['data-color']
            if colors is None or color in colors:
                results.append(ModelColor(colorId, color, node))
        return results

    def checkSingleModel(self, size, modelId ):
        result = None
        sizeSelectorList = self.soup.find("div", {"class": "sizes__wrapper", "data-id": modelId}).findAll("li", {"class": "sizes__size"})
        for info in sizeSelectorList:
            sizeLabel = info.find("span", {"class": "sizes__info"}).get_text()
            sizeStockLabel = info.find("span", {"class": "sizes__stock__info"}).get_text()
            if sizeLabel == size and sizeStockLabel != "0 disponibili": 
                result = DataStockInfo(info, sizeLabel, sizeStockLabel)
                # results.append(DataStockInfo(info, sizeLabel, sizeStockLabel, modelColor))
        return result

    def checkAvailability(self, size, colors):
        if self.soup is None:
            raise Exception("Sorry, soup is not set")

        results = []
        modelColors = self.getModelColors(colors)
        # [print(c) for c in modelColors]
        if len(modelColors) == 0:
            dataModelId = self.soup.find("input", {"class": "js-default-model"})
            res = self.checkSingleModel(size, dataModelId.attrs['data-model-id'])
            if res is not None:
              results.append(res)
            return results

        for modelColor in modelColors:
            res = self.checkSingleModel(size, modelColor.id)
            if res is not None:
              results.append(res)
        return results


class ModelColor:
    def __init__(self, id, color, node):
        self.id = id
        self.color = color
        self.node = node

    def __str__(self):
        return 'id: {} - color: {}'.format(self.id, self.color)


class DataStockInfo:
    def __init__(self, info, size, stock, color = None):
        self.info = info
        self.size = size
        self.stock = stock
        self.color = color

    def __str__(self):
        return 'size: {} - stock: {} - color: {}\n-----------------------------\ninfo: {}\n-----------------------------\n'.format(self.size, self.stock, self.color, self.info)
