from urllib.request import urlopen
from urllib.parse import *
from urllib.error import *
import time
import string
from bs4 import BeautifulSoup
import re
import os
import io
import nltk

HYPERLINK_PREFIX = "https://en.wikipedia.org/wiki/"


class WebCrawler(object):
    def __init__(self, seedUrl, maxDepth):

        # Initialization block.

        self.seedUrl = seedUrl
        self.maxDepth = maxDepth
        self.visitedUrl = []
        self.filenameCounter = 1
        self.depth = 1

    def writeContents(self, content, filename):

        # writes the content into the file with the given filename.
        print("This is the file name to be written / updated : ", filename)
        if os.path.isfile(filename):
            with open(filename, 'a') as g:
                g.write(content)
                g.write("\n")
                g.close()
        else:
            with open(filename, 'w') as h:
                h.write(content)
                h.write("\n")
                h.close()

    def writeIntoFileOperation(self, link, html_object):
        print("Writing document" + str(link) + "into file...")

        # Creates the directories for files with crawled links and raw html files.

        if not os.path.exists("Crawled_Files_Task1"):
            os.makedirs("Crawled_Files_Task1")
        if not os.path.exists("./Crawled_Files_Task1/Raw_Html_Task1"):
            os.makedirs("./Crawled_Files_Task1/Raw_Html_Task1")
        # tempfileName = re.sub('[\/:*?"<>|%]',"",tempfileName)
        link = link.replace("/", "_")
        self.filenameCounter += 1
        # html = html_object.prettify().encode('UTF-8')
        html = html_object

        # writes raw html file into the text file (after creating new text files)
        filename = str(link) + ".txt"
        if os.path.isfile("./Crawled_Files_Task1/Raw_Html_Task1/" + filename):
            filename = str(link) + str(self.filenameCounter) + ".txt"
            with open("./Crawled_Files_Task1/Raw_Html_Task1/" + filename, 'w', encoding='utf8') as f:
                f.write(html)
                f.close()
        else:
            with open("./Crawled_Files_Task1/Raw_Html_Task1/" + filename, 'w', encoding='utf8') as f:
                f.write(html)
                f.close()

    def getTextContent(self, soupObject):
        print("Extracting Text Content...")
        try:
            # Processes the text content , generates a clean corpus by tokenizing.

            for removeTag in soupObject(["script", "style", "table", "head"]):
                removeTag.decompose()
            for imageReference in soupObject.findAll("div", {
                "class": ["thumbinner", "mw-jump", "toc", "reflist columns references-column-width", "thumbcaption",
                          "plainlinks hlist navbar mini"]}):
                imageReference.decompose()
            for conSub in soupObject.findAll("div", {"id": "siteSub"}):
                conSub.decompose()
            for imagetag in soupObject.findAll("img"):
                imagetag.decompose()
            for editSection in soupObject.findAll("span", {"class": "mw-editsection"}):
                editSection.decompose()
            for imageHyperLink in soupObject.findAll("a", {"class": "image"}):
                imageHyperLink.decompose()
            for navigationLink in soupObject.findAll("div", {"role": ["navigation", "note"]}):
                navigationLink.decompose()
            for citationNumLink in soupObject.findAll("sup"):
                citationNumLink.decompose()
            for referenceLink in soupObject.findAll("ol", {"class": "references"}):
                referenceLink.decompose()

            html_text = soupObject.get_text()

            index_see_also = html_text.rfind('See also')
            index__references = html_text.find('References')

            if index_see_also >= 0:
                html_text = html_text[:index_see_also]
            elif index__references >= 0:
                html_text = html_text[:index__references]
            formattedext = self.format_text_Input(html_text)
            return formattedext

        except:
            print("Could not process.")

    def format_text_Input(self, rawTextData):
        print("Formatting Text Content...")
        # Removes the punctuations from the text.
        rawTextData = re.sub(r'[@_!\s^&*?#=+$~%:;\\/|<>(){}[\]"\']', ' ', rawTextData)
        rawTextData = rawTextData.lower()
        WordsinText = []
        r = re.compile(r"^(?=.*?\d)\d*[.,]?\d*$")
        # Takes care of the numbers and does not remove the commas and decimals appearing in them.
        # Makes sure the valid comma , decimal and dash in the word are not removed.
        for i in rawTextData.split():
            i = i.lower()
            if r.match(i):
                i = self.processWordEnd(i)
                if i != "." and i != "-" and i != ",":
                    WordsinText.append(i)
            else:
                if i[0] == ",":
                    if len(i) > 1:
                        i = i[1:]
                        i = self.processWordEnd(i)
                        if i != "." and i != "-" and i != ",":
                            WordsinText.append(i)
                elif i[0] == "-":
                    if len(i) > 1:
                        i = i[1:]
                        i = self.processWordEnd(i)
                        if i != "." and i != "-" and i != ",":
                            WordsinText.append(i)
                elif i[0] == ".":
                    if len(i) > 1:
                        i = i[1:]
                        i = self.processWordEnd(i)
                        if i != "." and i != "-" and i != ",":
                            WordsinText.append(i)
                else:
                    i = self.processWordEnd(i)
                    if i != "." and i != "-" and i != ",":
                        WordsinText.append(i)
        processedWordList = list(filter(lambda w: w != "", WordsinText))
        spacedWordList = " ".join(processedWordList)
        return spacedWordList

    def processWordEnd(self, sequence):
        if sequence[len(sequence) - 1] == ",":
            return sequence[:len(sequence) - 1]
        if sequence[len(sequence) - 1] == "-":
            return sequence[:len(sequence) - 1]
        if sequence[len(sequence) - 1] == ".":
            return sequence[:len(sequence) - 1]
        return sequence

    def crawl(self, hyperlink_to_crawl):
        print("Crawling new Document : ", hyperlink_to_crawl)
        print("depth", self.depth)
        nextLevelHyperlink = []
        # Crawls the given hyperlink and return the hyperlinks in next level.
        final_hyperlink_to_crawl = HYPERLINK_PREFIX + hyperlink_to_crawl
        currentPage = urlopen(final_hyperlink_to_crawl).read()
        soupObject = BeautifulSoup(currentPage, 'lxml')
        file_text = self.getTextContent(soupObject)
        self.writeIntoFileOperation(hyperlink_to_crawl, file_text)
        for hyperLink in soupObject.find_all('a', href=re.compile("^/wiki/")):
            linkHref = hyperLink.get('href')
            linkHref = linkHref.split('wiki/')[1]
            if ("#" in linkHref) and (":" not in linkHref) and ("Main_Page" not in linkHref):
                indexRemove = linkHref.index("#")
                linkHref = linkHref[:indexRemove]
                if linkHref not in self.visitedUrl and (linkHref not in nextLevelHyperlink):
                    nextLevelHyperlink.append(linkHref)
            if ("#" not in linkHref) and (":" not in linkHref) and ("Main_Page" not in linkHref):
                if (linkHref not in self.visitedUrl and (linkHref not in nextLevelHyperlink)):
                    nextLevelHyperlink.append(linkHref)
        return nextLevelHyperlink

    def crawlerOperationController(self):

        # controls the crawling for the current level of hyperlinks.

        nextLevelUrl = []
        currentLevelUrl = []
        currentLevelUrl.append(self.seedUrl)
        self.depth = 1
        while currentLevelUrl and self.depth <= self.maxDepth and len(self.visitedUrl) < 1000:
            pageUrl = currentLevelUrl.pop(0)
            if pageUrl not in self.visitedUrl:
                resultCrawl = []
                time.sleep(1)
                self.visitedUrl.append(pageUrl)
                resultCrawl = self.crawl(pageUrl)[:]
                nextLevelUrl.extend(resultCrawl)
            if len(currentLevelUrl) == 0:
                currentLevelUrl = nextLevelUrl[:]
                nextLevelUrl = []
                self.depth = self.depth + 1


if __name__ == "__main__":
    # Enter in order ==> URL , Maximum Depth Possible in WebCrawler

    crawler = WebCrawler('Green_Energy', 6)
    crawler.crawlerOperationController()
