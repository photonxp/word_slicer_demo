#!/usr/bin/python


"""
to do:
*Move input handlers to another module.
*Handle the input continously until EOF.
*Rename the variables used.
*Join the list of words sliced.
"""

'''
done:
*Modified _begin_partial, _cut_and_part methods for common machine and machine3.
'''

"""Define operations for different indications on letters"""

letter_marked = 'r'
partial = {'previous':'STORED_PREVIOUS','readed':letter_marked}

previous_partial = partial['previous']

SLICE_STATE_1 = ['',[letter_marked,'B'],'SliceMachine1']
SLICE_STATE_2 = [previous_partial,[letter_marked,'B'],'SliceMachine2']
SLICE_STATE_3 = [previous_partial,[letter_marked,'I'],'SliceMachine3']

def slice_line(line,prev_slice_result,cutted_list):
    parsed = parse_line(line)
    sm = package_handler(prev_slice_result[1],parsed)
    slice_result, cl = result_handler(res,cutted_list)

def parse_line(line):
    splitter = "   "
    splitted = line.split(splitter)
    print "splitted:", splitted
    #parsed = (splitted[0], splitted[1])
    return splitted[0],splitted[1]

def repack_parsed(slice_res, parsed_sequence):
    cutted,partial = slice_res[1]
    return partial,parsed_sequence

def package_handler(previous_partial, parsed_sequence):
    assert previous_partial is not None
    if '' == previous_partial:
        sm = SliceMachine1(parsed_sequence)
    if '' != previous_partial:
        if 'B' == readed_sequence[1]:
            sm = SliceMachine2(previous_partial, parsed_sequence)
        if 'I' == readed_sequence[1]:
            sm = SliceMachine3(previous_partial, parsed_sequence)
    
    sm.do_slice()
    return sm

def result_handler(res,cutted_list=[]):
    assert len(res) > 0
    if '' != res[0]:
        cutted_list.append(res[0])
    return (res,cutted_list)


class CommonMachine():
    def _set_readed_partial(self, readed_sequence=None):
        if readed_sequence is not None:
            self.readed_partial = readed_sequence[0]
        else:
            self.readed_partial = self.readed_sequence[0]
            
    def _begin_partial(self, readed_sequence=None):
        self.new_partial = self.readed_partial

    def _cut_and_part(self):
        self._set_readed_partial()
        self._cut_previous()
        self._begin_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

    def do_slice(self):
        pass

class SliceMachine1(CommonMachine):
    """slice when no need to handle existed word partial"""
    def __init__(self, readed_sequence=None):
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence
            print "self.readed_sequence:", self.readed_sequence

    def _cut_previous(self):
        self.cutted = ''

    def do_slice(self):
        return self._cut_and_part()

class SliceMachine2(CommonMachine):
    """slice when need to handle existed word partial"""
    def __init__(self, partial=None, readed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence
            print "self.readed_sequence:", self.readed_sequence

    def _cut_previous(self):
        self.cutted = self.previous_partial

    def do_slice(self):
        return self._cut_and_part()

class SliceMachine3(CommonMachine):
    """
    slice when need to handle existed word partial
     and append it with prevous partial to generate new partia
    """
    def __init__(self, partial=None, readed_sequence=None):
        if partial is not None:
            self.previous_partial = partial
        if readed_sequence is not None:
            self.readed_sequence = readed_sequence
            print "self.readed_sequence:", self.readed_sequence

    def _cut_previous(self):
        self.cutted = ""

    def _append_partial(self, readed_sequence=None):
        self._begin_partial(readed_sequence)
        self.new_partial = self.previous_partial + self.readed_partial
        
    def _cut_and_part(self):
        self._set_readed_partial()
        self._cut_previous()
        self._append_partial()
        self.slice_result = [self.cutted, self.new_partial]
        return self.slice_result

    def do_slice(self):
        return self._cut_and_part()


if __name__ == "__main__":

    print 'OK'

    cutted_list =[]

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
    print "sm.new_partial:",sm.new_partial
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
