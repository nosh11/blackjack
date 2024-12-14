class aa:
    def __init__(self):
        self.list=[]
        self.list.append(bb())

    def cc(self):
            print(self.list[0].dd())

class bb:
     def dd(self):
          print(1)
          return 2

a =aa()
a.cc()
