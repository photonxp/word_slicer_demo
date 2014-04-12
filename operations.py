#!/usr/bin/python


"""
to do:
*Join() the list of words sliced.
*Move the test statements to unittest.
"""

'''
done:
*Remov class SliceMachine1 and renamed SliceMachine2 to SliceMachine1, SliceMachine3 to SliceMachine2
'''

"""Define operations for various repeated marks on letters"""

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

'''

    readed_sequence = ['m','B']
    sm1 = SliceMachine1(readed_sequence)
    rs = sm1.do_slice()
    print rs
    cl = result_handler(rs, cutted_list)[1]
    print cl

    partial_2 = 'haha'
    readed_sequence = ['s','B']
    sm2 = SliceMachine2(partial_2,readed_sequence)
    rs = sm2.do_slice()
    print rs
    cl = result_handler(rs, cl)[1]
    print cl

    partial_3 = 'lala'
    parsed_sequence = ['y','I']
    sm3 = SliceMachine3(partial_3, parsed_sequence)
    rs = sm3.do_slice()
    print "sm3.previous_partial:",sm3.previous_partial
    print "sm3.new_partial:",sm3.new_partial
    cl = result_handler(rs, cl)[1]
    print cl

    p_partial=''
    readed_s=['k','B']
    sm = package_handler(p_partial, readed_s)
    print sm.slice_result
    #print "sm.previous_partial:",sm.previous_partial
    print "sm.new_partial:",sm.new_partial
    cl = result_handler(sm.slice_result, cl)[1]
    print cl
    
    
    p_partial='zz'
    readed_s=['u','B']
    sm = package_handler(p_partial, readed_s)
    print sm.slice_result
    cl = result_handler(sm.slice_result, cl)[1]
    print cl
    
    p_partial='m'
    readed_s = ['v','I']
    sm = package_handler(p_partial, readed_s)
    print sm.slice_result
    cl = result_handler(sm.slice_result, cl)[1]
    print cl
    
    pl = parse_line("x   I")
    print pl
    
    # slice line
    line = "r   B"
    prev_slice_result = ('pa','xxx')
    cutted_list = ['mmm']
    res = slice_line(line, prev_slice_result, cutted_list)
    print res
    
    # slice lines
    lines = file_handler("/home/linnan/IT/python_projects/various_codes/nlp/word_slice/data")
    prev_slice_result = ['cc','pp']
    cutted_list = ['www']
    cl = slice_lines(lines,prev_slice_result,cutted_list)
    print cl 
    
'''
