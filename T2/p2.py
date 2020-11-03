# research_members: use it
# relation_qty: use it
# at_least_friends: use it
# at_least_not_friend_of: use it
# return: maximize number of researchers
# Si lo hago con una matriz puedo hacerlo en n^2
# Si la matriz es simetrica puedo hacerlo en n*log(n)
# la matriz es simetrica porque es sin direccion
import math
from queue import PriorityQueue

research_members, relation_qty, at_least_friends, at_least_not_friend_of = (
    3,
    1,
    1,
    1,
)

researchers_relations = [
    frozenset((0, 1)),
]


def input_relation_generator(relation_qty):

    for _ in range(relation_qty):
        yield frozenset(map(lambda x: int(x) - 1, input().strip().split(" ")))


class QueueNode:
    def __init__(self, researcher, min_friends: int, max_friends: int):
        self.researcher = researcher
        self.min_friends = min_friends
        self.max_friends = max_friends

    @property
    def priority_points(self):
        friends = len(self.researcher.friends)
        if friends < self.min_friends:
            return math.inf
        return max(friends - self.max_friends, 0)

    def __lt__(self, other):
        return self.priority_points < other.priority_points


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

    def __hash__(self):
        return hash(self.relation)

    def __eq__(self, other):
        return self.relation == other.relation


class ResearchRelationGraph:
    def __init__(
        self,
        research_members,
        relation_qty,
        at_least_friends,
        at_least_not_friend_of,
    ):
        self.research_members = research_members
        self.relation_qty = relation_qty
        self.at_least_friends = at_least_friends
        self.at_least_not_friend_of = at_least_not_friend_of
        self.relations = set()
        self.researchers = list()
        for index in range(self.research_members):
            self.researchers.append(Researcher(index))
        super().__init__()

    def populate(self, researchers_relations):
        for relation in researchers_relations:
            relation = Relation(frozenset(relation))
            self.relations.add(relation)
            for researcher in relation.relation:
                self.researchers[researcher].relations.add(relation)
                self.researchers[researcher].friends.add(
                    set(relation.relation - {researcher}).pop()
                )

    def solve_max_researchers(self):

        pass


research_members, relation_qty, at_least_friends, at_least_not_friend_of = map(lambda x: int(x), input().strip().split(" "))
researchers_relations = input_relation_generator(relation_qty)

graph = ResearchRelationGraph(
    research_members, relation_qty, at_least_friends, at_least_not_friend_of
)

graph.populate(researchers_relations)

researchers = PriorityQueue()

memory = list()

for researcher in graph.researchers:
    wrap = QueueNode(researcher, at_least_friends, at_least_not_friend_of)
    researchers.put(wrap)
    memory.append(wrap)

related = set()
excluded = set()
researcher_stack = list()

while not researchers.empty():
    researcher = researchers.get()
    points = researcher.priority_points
    current_researcher = researcher.researcher
    friends_already_in = current_researcher.friends & related
    friends_remainding = current_researcher.friends - related
    amount_of_friends = len(current_researcher.friends)
    if amount_of_friends < graph.at_least_friends:
        excluded = excluded | {current_researcher.identifier}
    else:
        related.add(current_researcher.identifier)
        min_points = math.inf
        reference = None
        for researcher_id in friends_remainding - excluded:
            friend = memory[researcher_id]
            if friend.priority_points < min_points:
                min_points = friend.priority_points
                reference = friend
        if reference is not None:
            related = related | {reference.researcher.identifier}
    researcher_stack.append(researcher)


print(len(related))

# Output: max number of researchers
