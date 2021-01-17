from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type, Dict, Union
from common.database import Database

T = TypeVar('T', bound='Model')

class Model(metaclass=ABCMeta):
    collection: str
    _id: str #abstract properties for still getting the error

    def __init__(self,*args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self) :
        Database.remove(self.collection, {"_id" : self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T: #item.get_by_id()->item , alert.get_by_id()->alert
        return cls.find_one_by("_id", _id)

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T: #item.find_one_by('url', 'http://blala,com')
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str,  value: Union[str, Dict])  -> T:  # item.find_one_many('url', 'http://blala,com')
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute : value})]