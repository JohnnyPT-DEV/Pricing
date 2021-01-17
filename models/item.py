import requests
import re
import uuid
from typing import Dict
from bs4 import BeautifulSoup
from models.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: str
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float :
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d*\.\d\d)")  # at least two numbers in front of the period
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)

        return self.price

    def json(self) -> Dict:
        return {
            "_id" : self._id,
            "url" : self.url,
            "tag_name" : self.tag_name,
            "query" : self.query,
            "price": self.price
        }



