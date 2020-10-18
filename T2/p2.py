# research_members: use it
# relation_qty: use it
# at_least_friends: use it
# no_more_than_friends: use it
# return: maximize number of researchers
# Si lo hago con una matriz puedo hacerlo en n^2
# Si la matriz es simetrica puedo hacerlo en n*log(n)
# la matriz es simetrica porque es sin direccion 
# Se podra usar un polinomio?
# Convendra hacerlo aleotorizado?

research_members, relation_qty, at_least_friends, no_more_than_friends = (
    3,
    1,
    1,
    0,
)

researchers_relations = [frozenset((1, 2))]


def input_relation_generator(relation_qty):

    for _ in range(relation_qty):
        yield input().strip().split(" ")


class Researcher:
    def __init__(self, identifier):
        self.identifier = identifier
        self.friends = set()
        self.relations = set()
        super().__init__()

    def __eq__(self, other):
        return self.identifier == other.identifier


class Relation:
    def __init__(self, relation):
        self.relation = frozenset(relation)
        super().__init__()

    def __eq__(self, other):
        return self.relation == other.relation


class ResearchRelationGraph:
    def __init__(
        self,
        research_members,
        relation_qty,
        at_least_friends,
        no_more_than_friends,
    ):
        self.research_members = research_members
        self.relation_qty = relation_qty
        self.at_least_friends = at_least_friends
        self.no_more_than_friends = no_more_than_friends
        self.relations = set()
        self.researchers = list()
        for index in range(self.research_members):
            self.researchers.append(Researcher(index))
        super().__init__()

    def populate(self, researchers_relations):
        assert len(researchers_relations) == self.relation_qty
        for relation in researchers_relations:
            relation = Relation(frozenset(relation))
            self.relations.add(relation)
            for researcher in relation.relation:
                self.researchers[researcher].relations.add(relation)
                self.researchers[researcher].friends.add(
                    relation.relation - {researcher}
                )
    
    def solve_max_researchers(self):
        
        pass



# Output: max number of researchers
