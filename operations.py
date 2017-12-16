#!/usr/bin/python


"""This project defines operations for various repeated marks on letters, so that letters can be sliced into words."""

'''
todo:

'''

'''
done:
*Fix test methods test_init, test_take_machine, test_slice_lines for ServerTest, though root causes of the test failure are still unclear.
'''


class StateMachineSingletonFactory():
    def __init__(self):
        self.MACHINE_1_IS_SINGLE = False
        self.MACHINE_2_IS_SINGLE = False
        self.mark = ''
        
    def dispatch_machine(self,mark):
        """get the proper slice machine after check and set it successfully"""
        self.mark = mark
        self.set_slice_machine()
        return self.sm
        
    def set_slice_machine(self):
        mark = self.mark

        if 'B' == mark:
            self.set_machine_1_singleton()
        if 'I' == mark:
            self.set_machine_2_singleton()  
        
    def set_machine_1_singleton(self):
        if self.MACHINE_1_IS_SINGLE == False:
            self.slicemachine1 = SliceMachine1()
            self.MACHINE_1_IS_SINGLE = True
        self.sm = self.slicemachine1
        
    def set_machine_2_singleton(self):
        if self.MACHINE_2_IS_SINGLE == False:
            self.slicemachine2 = SliceMachine2()
            self.MACHINE_2_IS_SINGLE = True
        self.sm = self.slicemachine2

class CommonMachine():
    def __init__(self, partial=None, parsed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if parsed_sequence is not None:
            self.parsed_sequence = parsed_sequence
        print "Hi, I'm %s, I am called........." % self.__class__.__name__

    def _set_readed_partial(self):
        self.readed_partial = self.parsed_sequence[0]
            
    def do_slice(self):
        print "Hi, I'm %s, I am doing the slice........." % self.__class__.__name__
        self._cut_previous()
        self._set_readed_partial()
        self._set_new_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

class SliceMachine1(CommonMachine):
    """Machine to cut word"""

    def _cut_previous(self):
        self.cutted = self.previous_partial
    
    def _set_new_partial(self):
        self.new_partial = self.readed_partial

class SliceMachine2(CommonMachine):
    """Machine to join word"""

    def _cut_previous(self):
        self.cutted = ""

    def _set_new_partial(self):
        self.new_partial = self.previous_partial + self.readed_partial

if __name__ == "__main__":
    print 'OK'

