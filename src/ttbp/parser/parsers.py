import requests
import os
import json
import pickle

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as BS

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/87.0.4280.141 Safari/537.36"
)
PREVIEW_URL = "https://news.tut.by/geonews/{}/"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseParser(ABC):

    def __init__ (self, user_agent :str) -> None:
        self.user_agent = user_agent if user_agent is not None else DEFAULT_USER_AGENT

    def get_page (self, url):
        response = requests.get (
            url,
            headers={
                "User-Agent": self.user_agent
            }
        )
        if response.status_code == 200:
            return BS (response.text, features = "html.parser")
        raise ValueError ("response not 200")
        

    @abstractmethod
    def save_to_json(self, name: str) -> None:
        """Save news to file
        :param name: file name
        :type name: str
        """
    @abstractmethod
    def save_to_file(self, name: str) -> None:
        """Save news to json file
        :param name: file name
        :type name: str
        """


class Preview(BaseParser):

    def __init__ (self, **kwargs):
        super().__init__(kwargs.get("user_agent"))
        self.links = []
        self.city = kwargs.get("city") or Minsk

    def get_links (self):
        try:
            html = self.get_page (PREVIEW_URL.format(self.city))
        except ValueError:
            print ("error2")
            self.links = []
        else: 
            box = html.find ("div", attrs = {"class": "news-section m-rubric"})
            if box is not None:
                divs = box.find_all (
                    "div", attrs = {"class": "news-entry big annoticed time ni"}
                )
                for div in divs: 
                    link = div.find("a", attrs={"class": "entry__link"})
                    self.links.append(link.get("href"))

            else: 
                print ("error 3")
                self.links = []

    def save_to_file(self,name):
        path = os.path.join(BASE_DIR, name + ".bin")
        pickle.dump(self.links, open(path, "wb"))
    
    def save_to_json(self,name):
        path = os.path.join(BASE_DIR, name + ".json")
        json.dump(self.links, open(path, "w"))


if __name__ == "__main__":
    parser = Preview(city = "brest")
    parser.get_links()
    parser.save_to_json("tmp_links_brest")
    parser.save_to_file("tmp_links_brest")

