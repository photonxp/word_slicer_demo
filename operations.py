#!/usr/bin/python


"""This project defines operations for various repeated marks on letters, so that letters can be sliced into words."""

'''
todo:

'''

'''
done:
*Remov class SliceMachine1 and renamed SliceMachine2 to SliceMachine1, SliceMachine3 to SliceMachine2
*Join() the list of words sliced.
*Move the test statements to unittest.
'''

class StateMachineSingletonFactory():
    def __init__(self):
        self.MACHINE_1_IS_SINGLE = False
        self.MACHINE_2_IS_SINGLE = False
        
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
    def _set_readed_partial(self, parsed_sequence=None):
        if parsed_sequence is not None:
            self.readed_partial = parsed_sequence[0]
        else:
            self.readed_partial = self.parsed_sequence[0]
            
    def _begin_partial(self, parsed_sequence=None):
        self.new_partial = self.readed_partial

    def _cut_and_part(self):
        self._cut_previous()
        self._set_readed_partial()
        self._begin_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

    def do_slice(self):
        pass

class SliceMachine1(CommonMachine):
    """slice when need to handle existed word partial"""
    def __init__(self, partial=None, parsed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if parsed_sequence is not None:
            self.parsed_sequence = parsed_sequence
        print "Hi, I'm SliceMachine1, I am called........."

    def _cut_previous(self):
        self.cutted = self.previous_partial

    def do_slice(self):
        print "Hi, I'm SliceMachine1, I am doing the slice........."
        return self._cut_and_part()

class SliceMachine2(CommonMachine):
    """
    Slice when need to handle existed word partial
     and append it with prevous partial to generate new partial.
    """
    def __init__(self, partial=None, parsed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if parsed_sequence is not None:
            self.parsed_sequence = parsed_sequence
        print "Hi, I'm SliceMachine2, I am called........."

    def _cut_previous(self):
        self.cutted = ""

    def _append_partial(self, readed_sequence=None):
        self.new_partial = self.previous_partial + self.readed_partial
        
    def _cut_and_part(self):
        self._cut_previous()
        self._set_readed_partial()
        self._append_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

    def do_slice(self):
        print "Hi, I'm SliceMachine2, I am doing the slice........."
        return self._cut_and_part()


if __name__ == "__main__":

    print 'OK'


