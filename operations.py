#!/usr/bin/python


"""
to do:
*Push into git
*Add parent class SliceMachine for various SliceMachines. So some code can be reused.
"""

'''
Added CommonMachine Class to hold common methods
Move _begin_partial in child classes to CommonMachine 
'''


"""Define operations for different indications on letters"""

class CommonMachine():
    def _begin_partial(self, readed_sequence=None):
        if readed_sequence is not None:
            self.new_partial = readed_sequence[0]
        else:
            self.new_partial = self.readed_sequence[0]

class SliceMachine1(CommonMachine):
    """slice when no need to handle existed word partial"""
    def __init__(self, readed_sequence=None):
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence

    def slice_only_partial(self):
        self._begin_partial()
        self.slice_result = [self.new_partial]
        return self.slice_result

class SliceMachine2(CommonMachine):
    """slice when need to handle existed word partial"""
    def __init__(self, partial=None, readed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence
            print "self.readed_sequence:", self.readed_sequence

#    def _begin_partial(self, readed_sequence=None):
#        if readed_sequence is not None:
#            self.new_partial =  readed_sequence[0]
#        else:
#            self.new_partial = self.readed_sequence[0]

    def _cut_previous(self):
        self.cutted = self.previous_partial

    def slice_cutted_and_partial(self):
        self._cut_previous()
        self._begin_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

class SliceMachine3():
    """slice when need to handle existed word partial and append it with new partial"""
    def __init__(self, partial=None, readed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence
            print "self.readed_sequence:", self.readed_sequence

    def _append_partial(self, readed_sequence=None):
        if readed_sequence is not None:
            self.new_partial = self.previous_partial + readed_sequence[0]
        else:
            self.new_partial = self.previous_partial + self.readed_sequence[0]

    def slice_to_append(self):
        self._append_partial()
        self.slice_result = [self.new_partial]
        return self.slice_result


if __name__ == "__main__":

    print 'OK'


    readed_sequence = ['m','B']
    sm1 = SliceMachine1(readed_sequence)
    rs = sm1.slice_only_partial()
    print rs

    partial_2 = 'haha'
    readed_sequence = ['s','B']
    sm2 = SliceMachine2(partial_2,readed_sequence)
    rs = sm2.slice_cutted_and_partial()
    print rs

    partial_3 = 'lala'
    readed_sequence = ['y','I']
    sm3 = SliceMachine3(partial_3, readed_sequence)
    rs = sm3.slice_to_append()
    print rs
    

