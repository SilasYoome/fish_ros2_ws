from demo_python_package.person_node import PersonMode

class WriterMode(PersonMode):
    def __init__(self, name:str,age:int,book:str) -> None:
        print('WriterNode __init__ 方法被調用了')
        super().__init__(name,age) # super用於調用父類方法__init__
        self.book = book


def main():
    node = WriterMode('超級英雄',18,'論快速入獄')
    node.eat('青椒炒肉絲')