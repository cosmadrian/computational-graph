from threading import Semaphore
from threading import Event, Lock
from threading import Thread

class Node(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.__children = []
        self.__parents = []

        self.parents_done = None
        self.work_done = Event()
        self.received_input = Event()

        self.output_ = {}
        self.inputs = {}
        self.input_counter = 0
        self.inputs_lock = Lock()

    @property
    def children(self):
        return self.__children

    @property
    def parents(self):
        return self.__parents

    def add_children(self, children):
        self.__children += children
        for child in children:
            child.add_parents([self])

    def add_parents(self, parents):
        self.__parents += parents

    def compile(self):
        self.parents_done = Semaphore(0)
        try:
            self.start()
        except RuntimeError as e: pass


    @property
    def output(self):
        self.work_done.wait()
        self.work_done.clear()
        return self.output_


    def put_input(self, parent_input):
        with self.inputs_lock:
            self.inputs = {**self.inputs, **parent_input}
            self.parents_done.release()
            self.received_input.set()

    def work(self):
        print('waiting for release')
        for _ in range(len(self.parents)): self.parents_done.acquire()
        print('released')

        self.received_input.wait()
        self.received_input.clear()
        self.do_work()
        self.work_done.set()

        for child in self.__children:
            child.put_input(self.output_)

        self.parents_done = Semaphore(0)
        self.inputs = {}

    def do_work(self):
        raise NotImplementedError

    def run(self):
        while True:
            self.work()


class LensModel(object):
    def __init__(self, _input, output):
        self.input_node = _input
        self.output_node = output

    def compile(self):
        self.__compile(self.input_node)

    def __compile(self, start_node):
        start_node.compile()
        for child in start_node.children:
            self.__compile(child)

    def forward(self, inputs):
        self.input_node.put_input(inputs)

    def __print_node(self, node):
        # needs some fixes
        print(node.name,
            [parent.name for parent in node.parents],
            [child.name for child in node.children])
        for child in node.children:
            self.__print_node(child)

    def summary(self):
        print('Name', 'Parents', 'Children')
        self.__print_node(self.input_node)
