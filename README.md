word_slicer_demo
================

A simple demo to show how to slice words for letters already marked with tags
 
Read the marked letters form ./data file

This demo can be used for NLP leaning.

    from server import Server
    sv = Server()
    sv.handle_data()

    # input ./data   
    # output: ['a', 'bc', '\n', 'def', 'gh']
