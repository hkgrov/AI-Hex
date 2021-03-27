import graphviz


class decision_tree_plot():
    def __init__(self, state):
        self.dot = graphviz.Digraph(name="Decision Tree")
        self.dot.attr(ranksep="2")
        self.ascii_value = 65
        self.edges = set()
        self.create_decision_tree(state, chr(self.ascii_value), self.ascii_value + 1, 0)
        

    
    def create_decision_tree(self, state, name, ascii_value, next_level_value):
        level_value = next_level_value
        next_level_value = next_level_value
        self.dot.node(name, str(state.total_wins) + " / " + str(state.num_visits))
        queue = state.children.copy()

        while queue:
            child = queue.pop()
            if(child.num_visits == 0):
                continue
            new_name = chr(ascii_value) + str(level_value)
            #self.dot.edge(name, new_name)
            self.edges.add(name +","+ new_name)
            next_level_value = self.create_decision_tree(child, new_name, ascii_value + 1, next_level_value)
            level_value += 1
        
        if state.parent_state == None:
            #self.dot.edges(self.edges)
            for ele in self.edges:
                nodes = ele.split(",")
                #print(nodes)
                self.dot.edge(nodes[0], nodes[1])
            #print(self.dot)
            #print(self.edges)
            self.dot.render()
        
        return level_value
