#!/usr/bin/python

"""
Handle the slicing requests and responses

At least, return the cutted list
"""

from operations import StateMachineSingletonFactory
from operations import SliceMachine2,SliceMachine3,CommonMachine

letter_marked = 'r'
partial = {'previous':'STORED_PREVIOUS','readed':letter_marked}

stored_previous_partial = partial['previous']


SLICE_STATE_2 = [stored_previous_partial,[letter_marked,'B'],'SliceMachine2']
SLICE_STATE_3 = [stored_previous_partial,[letter_marked,'I'],'SliceMachine3']

class Server():
    def __init__(self,cutted_list=[]):
        self.cutted_list = cutted_list
        self.stored_previous_partial = ''
        self.new_partial = ''
        self.singleton_factory = StateMachineSingletonFactory()
        
    def file_handler(self,data_path):
        self.data_path = data_path
        f = open(data_path,'r')
        self.lines = f.readlines()
        f.close()

    def slice_lines(self):
        # new line would be parsed as a new-line-word.      
        for line in self.lines:
            self.file_line = line
            if '\n' == line:
                self.cutted_list.append('\n')
                continue
        
            self.prepare_line(line)
            self.slice_line()
            self.handle_result()
            
    def prepare_line(self,line):
        line = line.rstrip('\n')
        self.prepared_line = line 

    def slice_line(self):
        self.parse_line(self.prepared_line)
        self.package_handler()

        
    def parse_line(self,line):
        splitter = "   " # or "\b{3}" for re module
        self.parsed_sequence = line.split(splitter)
        
    def package_handler(self):
        assert self.stored_previous_partial is not None
        self.take_machine()
        self.update_machine_data_before_slice()
        self.sm.do_slice()
        
    def take_machine(self):
        #SliceMachineSingletonFactory.get_state_machine
        self.mark = self.parsed_sequence[1]
        self.sm = self.singleton_factory.dispatch_machine(self.mark)   
        
    def update_machine_data_before_slice(self):
        self.sm.previous_partial = self.stored_previous_partial
        self.sm.parsed_sequence = self.parsed_sequence
            
    def handle_result(self):
        assert len(self.sm.slice_result) > 0
        self.slice_result = self.sm.slice_result
        self.update_server_data()
    
    def update_server_data(self):
        self.update_cutted_list()
        self.stored_previous_partial = self.slice_result[1]
        
    def update_cutted_list(self):
        cutted = self.sm.slice_result[0]
        #print "==update_cutted_list==", cutted
        if '' != cutted:
            self.cutted_list.append(cutted)

        
if __name__ == "__main__":
    sv = Server()
    data_path = "/home/linnan/IT/python_projects/various_codes/nlp/word_slice/data"
    sv.file_handler(data_path)
    sv.slice_lines()
    cutted_list = sv.cutted_list
    print cutted_list
    
    # ['a', 'bc', '\n', 'def', 'ab']
