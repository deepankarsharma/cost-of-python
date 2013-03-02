Steps to obtain timings and create table from data
--------------------------------------------------

python measure.py cpython.data
pypy measure.py pypy.data

python draw_table.py cpython.data cpython.png
python draw_table.py pypy.data pypy.png

Dependencies
------------

1. PyQt4
2. Numpy
3. blist

Blog entry accompanying this repo follows
-----------------------------------------

C programmers have the benefit of having a mental model for understanding the performance characteristics of their code. Working in a high level language like Python can take this luxury away from you. Good tools exist for identifying time and memory performance of existing codebases (line_profiler by Robert Kern - http://packages.python.org/line_profiler/ and guppy by  Sverker Nilsson - http://guppy-pe.sourceforge.net/). However you are largely on your own if you want to develop intuition for code that is yet to be written. Understanding the cost of basic operations in your Python implementation can help you cut down the design space at the design stage of your application development by ruling out designs that make extensive use of expensive operations. 

Why is this important you ask? Interactive applications appear responsive if they react to user behaviour within short periods of time. Some example of thresholds for user interaction are 

1. If you are targeting 60 fps in a multimedia application you have 16 milliseconds of processing time per frame. In this time you need to update state, figure out what is visible, and then draw it.
2. Well behaved applications will load up a functional screen that a user can interact with in under a second. Depending on your application you might need to create an expensive datastructure upfront before your user can interact with the application.
3. You run Gentoo / Arch. In this case obsessing over performance is a way of life.
