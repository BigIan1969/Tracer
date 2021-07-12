#MIT License
#
#Copyright (c) 2021 Ian Holdsworth
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from tracewrapper import tracewrapper
import opcode

#Show_Trace function just like you'd feed to sys.settrace()
def show_trace1(frame, event, arg):
    code = frame.f_code
    offset = frame.f_lasti
    print(f"Trace1| {event:10} | {str(arg):>4} |", end=' ')
    print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
    print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
    return show_trace1

#Another Show_Trace function just like you'd feed to sys.settrace()
def show_trace2(frame, event, arg):
    code = frame.f_code
    offset = frame.f_lasti
    print(f"Trace2| {event:10} | {str(arg):>4} |", end=' ')
    print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
    print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} | {code.co_name}")
    return show_trace2

#Show_Trace as a class
class TClass(tracewrapper.TracerClass):
    def trace(self, frame, event, arg):
        code = frame.f_code
        offset = frame.f_lasti
        print(f"Trace3| {event:10} | {str(arg):>4} |", end=' ')
        print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
        print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
        return self

#Demo fibanaci function to trace
def fib(n):
    i, f1, f2 = 1, 1, 1
    while i < n:
        f1, f2 = f2, f1 + f2
        i += 1
    return f1

#Instanciate the tracewrapper() class
tracer=tracewrapper.tracewrapper()

#Add our two demo show_trace functions
tracer.add(show_trace1)
tracer.add(show_trace2)

#Instanciate TClass() our inherited TracerClass()
tc=TClass()

#Add TracerClass's trace method to Tracer
tracer.add(tc.trace)

#Activate it
tc.start()

#Start tracing
tracer.start()

#Call our demo function
fib(6)

#Stop Tracing
tracer.stop()
