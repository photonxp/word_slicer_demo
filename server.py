#!/usr/bin/python

"""
Handle the slicing requests and responses

At least, return the cutted list
"""

from operations import StateMachineSingletonFactory
from operations import SliceMachine1, SliceMachine2, CommonMachine
import re
from copy import deepcopy


'''
Write the document as code
'''

partial = ['old_stored_partial','stored_partial']

SLICE_STATE_1 = ('stored_partial_value',['letter_tag','B'],'SliceMachine1')
SLICE_STATE_2 = ('stored_partial_value',['letter_tag','I'],'SliceMachine2')

class Server():
    """
    Parce data file. 
    Use ParcedDataHandler to call slice machines to handled the parced data
    """
    def __init__(self,cutted_list=[]):
        self.cutted_list = cutted_list
        self.old_partial = ''
        self.new_partial = ''
        self.singleton_factory = StateMachineSingletonFactory()
        
    def read_tag_file(self,data_path):
        self.data_path = data_path
        f = open(data_path,'r')
        self.filelines = f.readlines()
        f.close()

    def prepare_line(self,line):
        line = line.rstrip('\n')
        self.prepared_line = line 

    def simple_parse_line(self,line):
        splitter = "   " # 3 spaces
        self.parsed_sequence = tuple(line.split(splitter))
        
    def re_parse_line(self,line):
        delimiter = re.compile("\s{3}")
        self.parsed_sequence = tuple(re.split(delimiter, line))
        
    def parse_line(self,line):
        self.prepare_line(line)
        self.re_parse_line(self.prepared_line)
 
    def parse_lines(self):
        self.parsed_line_sequence_list = []
        for line in self.filelines:
            self.parse_line(line)
            self.parsed_line_sequence_list.append(self.parsed_sequence)

    def handle_data(self):
        self.read_tag_file("./data")
        self.parse_lines()
        print "self.parsed_line_sequence_list", self.parsed_line_sequence_list
        handler = ParcedDataHandler(parsed_line_sequence_list = self.parsed_line_sequence_list)  
        handler.slice_lines()
        print "handler.cutted_list", handler.cutted_list
        return handler

class ParcedDataHandler():
    """ Handle parced data in Server. Return slice result """
    def __init__(self, cutted_list=[], parsed_line_sequence_list=[]):
        self.cutted_list = deepcopy(cutted_list)
        self.parsed_line_sequence_list = deepcopy(parsed_line_sequence_list)
        # old_stored_partial is used to save old value 
        #     when stored_partial is updated 
        #     after SliceMachine.previous_partial return new partial value 
        self.old_stored_partial = ''
        # stored_partial is sent to SliceMachine.previous_partial
        #     and would receive new partial value 
        #     from SliceMachine.slice_result
        self.stored_partial = ''
        self.singleton_factory = StateMachineSingletonFactory()

    def get_machine(self, mark):
        sm = self.singleton_factory.dispatch_machine(mark)   
        return sm

    def update_cutted_list(self, sm):
        cutted = sm.slice_result[0]
        if '' != cutted:
            print "cutted in update_cutted_list:", cutted  
            self.cutted_list.append(cutted)
            
    def get_machine_result(self, sm):
        self.update_cutted_list(sm)
        self.old_stored_partial = self.stored_partial
        self.stored_partial = sm.slice_result[1]
        #self.cutted = sm.cutted
        
    def slice_line(self, parcedTuple):
        #self.handle_package(parcedTuple)
        assert self.stored_partial is not None
        mark = parcedTuple[1]
        sm = self.get_machine(mark)
        sm.__init__(self.stored_partial, parcedTuple)
        sm.do_slice()
        self.get_machine_result(sm)
        #return sm

    def slice_lines(self):
        # a new line in the data file would be eventually parsed as ("",)      
        # self.parsed_line_sequence_list should be already parced to a list of tuples
        for parcedLineTuple in self.parsed_line_sequence_list:
            if "" == parcedLineTuple[0]:
                self.cutted_list.append('\n')
                continue
            sm = self.slice_line(parcedLineTuple)
            
    def cutted_list_to_line(self):
        lines = ""
        for line in self.cutted_list:
            if "\n" != line:
                lines = lines.join([line, "\n"])
        return lines
        
if __name__ == "__main__":
    pass

    sv = Server()
    sv.handle_data()

    # input ./data    
    # output: ['a', 'bc', '\n', 'def', 'gh']
