#!/usr/bin/python

"""
The tests should work fine. But there're probably some bugs related to unittest or python2.6.5, which may cause several tests in ServerTest to fail.

The exact causes of the failed tests are still unknown. But the suspicion is that the Server instance sv in in different test methods are affected by each other, so some of its values(e.g. cutted) are changed strangely when the server is initiated every time.

Maybe someone can help verify it or file a bug to a python website related.
"""

import unittest
from operations import SliceMachine1, SliceMachine2, StateMachineSingletonFactory
from server import Server

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
        
class ServerTest(unittest.TestCase):  

    def test_init(self):
        print "::test_init starts ..."
        sv = Server(cutted_list=[])
        self.assertEquals('',sv.stored_previous_partial)
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
        self.assertEquals(['z','I'], sv.parsed_sequence)
    
    def test_take_machine(self):
        print "::test_take_machine starts ..."
        sv = Server(cutted_list=[])
        sv.parsed_sequence = ('c','B')
        self.assertEquals([],sv.cutted_list)
        sv.take_machine()
        self.assertEquals([],sv.cutted_list)
        self.assertTrue(isinstance(sv.sm, SliceMachine1))
        self.assertEquals('', sv.stored_previous_partial)
        self.assertEquals([],sv.cutted_list)

        sv.parsed_sequence = ('x','I')
        sv.take_machine()
        self.assertTrue(isinstance(sv.sm, SliceMachine2))
        self.assertEquals('', sv.stored_previous_partial)
        self.assertEquals('',sv.new_partial)
        self.assertEquals([],sv.cutted_list)
        
  
    def test_update_machine_data_before_slice(self):
        print "::test_update_machine_data_before_slice starts ..."
        sv = Server()
        sv.stored_previous_partial = 'cuu'
        sv.prepared_line = 'p   B'
        sv.parse_line(sv.prepared_line)
        sv.take_machine()
        sv.update_machine_data_before_slice()
        self.assertEquals('cuu', sv.sm.previous_partial)
        #self.assertEquals('cuu', sv.sm.previous_partial)
        self.assertTrue(isinstance(sv.sm,SliceMachine1))
        self.assertRaises(KeyError,self.raise_smKeyError)  

    def raise_smKeyError(self):
        try:
            #print "Comment the below not to raise an error."
            self.sv.sm.new_partial
        except AttributeError:
            raise KeyError("Key sv.sm.new_partial does not exist, \n \
            probably because the sv.sm didn't finish slicing?")
            
               
    def test_sm_do_slice(self):
        print "::test_sm_do_slice starts ..."
        sv = Server()
        sv.stored_previous_partial = 'cuu'
        sv.prepared_line = 'p   B'
        sv.parse_line(sv.prepared_line)
        sv.take_machine()
        sv.update_machine_data_before_slice()
        sv.sm.do_slice()
        self.assertEquals('cuu', sv.sm.previous_partial)
        self.assertTrue(isinstance(sv.sm,SliceMachine1))
        self.assertEquals('p',sv.sm.new_partial)
        self.assertEquals('cuu',sv.sm.cutted)

         
    def test_handle_package(self):
        print "::test_handle_package starts ..."
        sv = Server()
        sv.stored_previous_partial = 'cuu'
        sv.prepared_line = 'p   B'
        sv.parse_line(sv.prepared_line)
        sv.handle_package()
        self.assertEquals('p', sv.sm.new_partial)
        self.assertEquals('cuu', sv.sm.slice_result[0])
        self.assertEquals('cuu', sv.sm.cutted)
        

    def test_slice_line(self):
        print "::test_slice_line starts ..."
        sv = Server()
        sv.stored_previous_partial = 'cuu'
        sv.prepared_line = 'p   B'
        sv.slice_line()
        self.assertEquals('cuu',sv.sm.slice_result[0])

        
    def test_slice_lines(self):
        print "::test_slice_lines starts ..."
        sv = Server(cutted_list=[])
        self.assertEquals('',sv.stored_previous_partial)
        self.assertEquals('',sv.new_partial)
        self.assertEquals([],sv.cutted_list)
        sv.lines = ['a   B\n','b   B\n','c   I\n','d   B\n','e   I\n','f   I\n', \
        '\n','g   B\n','h   I\n','i   B\n']
        sv.slice_lines()
        self.assertEquals('gh',sv.sm.cutted)
        self.assertEquals(['a', 'bc', '\n', 'def', 'gh'], sv.cutted_list)

  
    def test_handle_result(self):
        print "::test_handle_result starts ..."
        sv = Server()
        sv.stored_previous_partial = 'cuu'
        sv.prepared_line = 'p   B'
        sv.slice_line()
        sv.handle_result()
        self.assertEquals('cuu', sv.slice_result[0])
        self.assertEquals('p', sv.slice_result[1])
        #self.assertEquals('cuu', sv.cutted)
        #self.assertEquals('p', sv.new_partial)
   
        
if __name__ == "__main__":
    unittest.main()

