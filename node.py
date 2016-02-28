class Node(object):

    TRUE = 't'
    FALSE = 'f'
    QUERY = '?'
    NOTHING = '-'

    def __init__(self, name):
        self.name = name
        self.status = self.NOTHING
        self.cpt = []
        self.index = None
        self.__children = []
        self.__parents = []
        return

    def __str__(self):
        return self.name

    def addCPT(self, cpt):
        self.cpt = cpt

    def addChild(self, node):
        self.__children.append(node)
        node.__parents.append(self)

    def children(self):
        return self.__children

    def parents(self):
        return self.__parents
