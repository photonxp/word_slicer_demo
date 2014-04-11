#!/usr/bin/python

from operations import start_partial, cut_last, append_partial

data_path = "./data"
file_r = open(data_path, "r")

lines=file_r.readlines()

tag_traslation_table = {"B":"SLICE","I":"APPEND"}
#wordpartial_status_pair_name = ("partial","status")
indacation_operations_map={
    "SLICE":[slice_word_partial],
    "APPEND":[append_partial]
    }


def start_new_partial(new_readed_sequece):
    """the map is like ("l","B"),("m","B") """
    new_partial =  new_readed_sequence[0]
    return new_partial

def cut_last(last_partial):
    last_cutted = last_partial
    return last_cutted

def append_last_partial(last_partial, new_readed_sequence):
    last_partial  += new_readed_sequence[0]
    return last_partial
