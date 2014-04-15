#!/usr/bin/python

"""
Handle the slicing requests and responses

At least, return the cutted list
"""

from operations import StateMachineSingletonFactory
from operations import SliceMachine1, SliceMachine2, CommonMachine
import re


'''
Write the document as code
'''

letter_marked = 'r'
partial = {'previous':'STORED_PREVIOUS','readed':letter_marked}

stored_previous_partial = partial['previous']


SLICE_STATE_1 = (stored_previous_partial,[letter_marked,'B'],'SliceMachine1')
SLICE_STATE_2 = (stored_previous_partial,[letter_marked,'I'],'SliceMachine2')

class Server():
    def __init__(self,cutted_list=[]):
        print "... Impossible ... Could cutted_list be changed?:", cutted_list 
        self.cutted_list = cutted_list
        print "Soooooo strange, am I [] or ['cuu']? :", self.cutted_list 
        self.stored_previous_partial = ''
        self.new_partial = ''
        self.singleton_factory = StateMachineSingletonFactory()
        print "Finished singleton_factory, am I changed at cutted_list? :", self.cutted_list 
        
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
        self.handle_package()

    def parse_line(self,line):
        self.re_parse_line(line)
        
    def simple_parse_line(self,line):
        splitter = "   " # 3 spaces
        self.parsed_sequence = line.split(splitter)
        
    def re_parse_line(self,line):
        delimiter = re.compile("\s{3}")
        self.parsed_sequence = re.split(delimiter, line)
        
    def handle_package(self):
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
        self.sm.mark = self.mark
            
    def handle_result(self):
        assert len(self.sm.slice_result) > 0
        self.slice_result = self.sm.slice_result
        self.update_server_data()
    
    def update_server_data(self):
        self.update_cutted_list()
        self.stored_previous_partial = self.slice_result[1]
        self.cutted = self.slice_result[0]
        
    def update_cutted_list(self):
        cutted = self.sm.slice_result[0]
        if '' != cutted:
            self.cutted_list.append(cutted)
            
    def sliced_list_to_line(self):
        lines = ""
        for line in self.cutted_list:
            if "\n" != line:
                lines = lines + line + "\n"
        return lines
            

        
if __name__ == "__main__":
    pass

    sv = Server()
    sv.parse_line("a   I")
    print sv.parsed_sequence
    
    # ['a', 'bc', '\n', 'def', 'ab']  ss

