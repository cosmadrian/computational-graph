from graph import Node, LensModel

class CustomNode(Node):
    ID = 1
    def __init__(self, name):
        Node.__init__(self, name)
        CustomNode.ID += 1
        self._id = CustomNode.ID

    def do_work(self):
        self.output_['x_' + str(self._id)] =  self._id


"""
    input ----- node1_branch1 ---- node2_branch1 --
        \                                           \
         \                                           \
           ----------- node1_branch2 ---------------- output_node

"""


input_node = CustomNode('input')
node1_branch1 = CustomNode('node1_branch1')
node2_branch1 = CustomNode('node2_branch1')
node1_branch2 = CustomNode('node1_branch2')
output_node = CustomNode('output')


input_node.add_children([node1_branch1, node1_branch2])
node1_branch1.add_children([node2_branch1])

node1_branch2.add_children([output_node])
node2_branch1.add_children([output_node])


model = LensModel(input_node, output_node)
print(model.summary())
model.compile()
model.forward({'1': 2})
print(output_node.output)
model.forward({'1': 2})
print(output_node.output)

