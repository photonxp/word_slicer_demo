#!/usr/bin/python

"""
Tests for Server, ParcedDataHandlerTest, and machine classes
"""

import unittest
from operations import SliceMachine1, SliceMachine2, StateMachineSingletonFactory
from server import Server, ParcedDataHandler

class MachineTests(unittest.TestCase):
    def setUp(self):
        self.sm1 = SliceMachine1()
        self.sm2 = SliceMachine2()
        
    def test_machine1_slice_without_pre_partial(self):
        print "test_machine1_slice_without_pre_partial starts ..."
        self.sm1.previous_partial = ''
        self.sm1.parsed_sequence = ('m','B')
        self.sm1.do_slice()
        self.assertEquals('', self.sm1.cutted)
        self.assertEquals('m', self.sm1.new_partial)
        
    def test_machine1_slice_with_pre_partial(self):
        self.sm1.previous_partial = 'haha'
        self.sm1.parsed_sequence = ('s','B')
        self.sm1.do_slice()
        self.assertEquals('haha', self.sm1.cutted)
        self.assertEquals('s', self.sm1.new_partial)
    
    def test_machine2_slice(self):
        self.sm2.previous_partial = 'lala'
        self.sm2.parsed_sequence = ('y','I')
        self.sm2.do_slice()
        self.assertEquals('', self.sm2.cutted)
        self.assertEquals('lalay', self.sm2.new_partial)

class ParcedDataHandlerTest(unittest.TestCase):
    def test__init__(self):   
        PARSED_LINE_SEQUENCE_LIST = [("a","B"),("b","B"),("c","I"),("d","B"), \
            ("e","I"),("f","I"),("",),("g","B"),("h","I"),("i","B")]
        handler = ParcedDataHandler(parsed_line_sequence_list=PARSED_LINE_SEQUENCE_LIST)
        self.assertEquals([], handler.cutted_list)
        self.assertEquals(PARSED_LINE_SEQUENCE_LIST, handler.parsed_line_sequence_list)
        self.assertEquals('', handler.old_stored_partial)
        self.assertEquals('', handler.stored_partial)
        self.assertEquals('', handler.singleton_factory.mark)

    def test_get_machine(self):
        handler = ParcedDataHandler()
        sm = handler.get_machine("B")
        self.assertEquals('SliceMachine1', sm.__class__.__name__)
        sm = handler.get_machine("I")
        self.assertEquals('SliceMachine2', sm.__class__.__name__)

    def test_update_cutted_list(self):
        handler1 = ParcedDataHandler()
        sm = handler1.get_machine("B")
        sm.__init__("a", ("b", "B"))
        sm.do_slice()
        handler1.update_cutted_list(sm)
        cutted_list = handler1.cutted_list 
        self.assertEquals(["a"], cutted_list)
        
        handler2 = ParcedDataHandler()
        sm = handler2.get_machine("I")
        sm.__init__("axx", ("b", "I"))
        sm.do_slice()
        self.assertEquals('', sm.cutted)
        self.assertEquals('axxb', sm.new_partial)
        self.assertEquals(['','axxb'], sm.slice_result)
        
        handler2.update_cutted_list(sm)
        cutted_list = handler2.cutted_list 
        self.assertEquals([], cutted_list)

    def test_get_machine_result(self):
        handler1 = ParcedDataHandler()
        sm = handler1.get_machine("B")
        sm.__init__("a", ("b", "B"))
        sm.do_slice()
        handler1.get_machine_result(sm)
        self.assertEquals(["a"], handler1.cutted_list)
        self.assertEquals("", handler1.old_stored_partial)
        self.assertEquals("b", handler1.stored_partial)
          
        handler2 = ParcedDataHandler()
        sm = handler2.get_machine("I")
        sm.__init__("a", ("b", "I"))
        sm.do_slice()
        handler2.get_machine_result(sm)
        self.assertEquals([], handler2.cutted_list)
        self.assertEquals("", handler2.old_stored_partial)
        self.assertEquals("ab", handler2.stored_partial)
    
    def test_slice_line(self):
        handler1 = ParcedDataHandler()
        handler1.slice_line(("b","B"))
        self.assertEquals([], handler1.cutted_list)
        self.assertEquals("", handler1.old_stored_partial)
        self.assertEquals("b", handler1.stored_partial)

    def test_slice_lines(self):
        PARSED_LINE_SEQUENCE_LIST = [("a","B"),("b","B"),("c","I"),("d","B"), \
            ("e","I"),("f","I"),("",),("g","B"),("h","I"),("i","B")]
        handler1 = ParcedDataHandler(parsed_line_sequence_list=PARSED_LINE_SEQUENCE_LIST)
        handler1.slice_lines()
        self.assertEquals(["a","bc","\n","def","gh"], handler1.cutted_list)

        
class ServerTest(unittest.TestCase):  
    def test_init(self):
        print "::test_init starts ..."
        sv = Server(cutted_list=[])
        self.assertEquals('',sv.old_partial)
        self.assertEquals('',sv.new_partial)
        self.assertTrue(isinstance(sv.singleton_factory,StateMachineSingletonFactory))
        self.assertRaises(KeyError,self.raise_svKeyError)  
        self.assertEquals([],sv.cutted_list)

    def raise_svKeyError(self):
        try:
            #print "Comment the below so not to raise an error." 
            self.sv.cutted
        except AttributeError:
            raise KeyError("Key sv.cutted does not exist, \n \
            probably because the sv didn't finish slicing or cutting?")

    def test_read_tag_file(self):
        sv = Server()
        sv.read_tag_file("./data")
        FILE_LINES = ['a   B\n', 'b   B\n', 'c   I\n', 'd   B\n', 'e   I\n', 'f   I\n', '\n', 'g   B\n', 'h   I\n', 'i   B\n']
        self.assertEquals(FILE_LINES, sv.filelines)

    def test_prepare_line(self):
        print "::test_prepare_line starts ..."
        sv = Server()
        line = 's   B\n'
        sv.prepare_line(line)
        self.assertEquals('s   B', sv.prepared_line)
      

    def test_parse_line(self):
        print "::test_parse_line starts ..."
        sv = Server()
        line = 'z   I'
        sv.parse_line(line)
        self.assertEquals(('z','I'), sv.parsed_sequence)

    def test_parse_lines(self):
        sv = Server()
        sv.read_tag_file("./data") 
        sv.parse_lines()
        PARSED_LINE_SEQUENCE_LIST = [("a","B"),("b","B"),("c","I"),("d","B"), \
            ("e","I"),("f","I"),("",),("g","B"),("h","I"),("i","B")]
        self.assertEquals(PARSED_LINE_SEQUENCE_LIST, sv.parsed_line_sequence_list)

    def test_handle_data(self):
        sv = Server()
        handler = sv.handle_data()
        self.assertEquals(['a', 'bc', '\n', 'def', 'gh'], handler.cutted_list)
        
if __name__ == "__main__":
    unittest.main()
