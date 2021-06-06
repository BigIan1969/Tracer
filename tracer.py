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

import sys
import types
class Tracer():
    """
    Tracer is a wrapper class for sys.settrace()
    """
    def __init__(self):
        self.functions=[]
        self.functionexclusions=[]
        self.moduleexclusions=[]
        self.filters={}

    def add(self, func):
        """Adds a a tracer function (see sys.trace()) or the TracerClass.trace() method"""
        if isinstance(func, types.FunctionType):
            self.functions.append(func)
            self.functionexclusions.append(func.__name__)
        elif isinstance(func, types.MethodType):
            self.functions.append(func)
            self.functionexclusions.append(func.__name__)
        else:
            assert type(func) is FunctionType, "Passed function is not a function or a method"

    def delete(self, func):
        """"Removes a trace function"""
        if isinstance(func, types.FunctionType):
            self.functions.remove(('func',func))
            self.functionexclusions.remove(func.__name__)
        elif isinstance(func, types.MethodType):
            self.functions.remove(('meth',func))
            self.functionexclusions.remove(func.__name__)

#filters
    def add_event_filter(self, func, event):
        """Adds a filter to a trace function or method"""
        if func in self.functions:
            if func not in self.filters:
                self.filters[func]=list()
            self.filters[func].append(event)
        else:
            assert func in self.functions, "Cannot add filter for function that hasn't been added"

    def delete_event_filter(self, func, event):
        """Removes a trace filter"""
        if func in self.functions:
            if func not in self.filters:
                self.filters[func]=list()
            if event in self.filters[func]:
                self.filters[func].remove(event)
        else:
            assert func in self.functions, "Cannot delete filter from function that hasn't been added"

    #returns true if filter is active
    def event_filter(self, func, event):
        """Returns True if the event for this function is being filtered"""
        assert func in self.functions, "Cannot filter for function that hasn't been added"
        if func not in self.filters:
            return False
        if event not in self.filters[func]:
            return False
        return True


#Function Exclusions
    def add_function_exclusion(self, ex):
        """Add a function to exclude from all trace functions or methods"""
        assert type(ex) is str, "Exclusion {ex} is not string"
        self.functionexclusions.append(ex)

    def delete_function_exclusion(self, ex):
        """Remove a function exclusion"""
        assert type(ex) is str, "Exclusion {ex} is not string"
        if ex in self.functionexclusions:
            self.functionexclusions.remove(ex)

    def function_excluded(self, ex):
        """Returns True if function is excluded"""
        if ex in self.functionexclusions:
            return True
        else:
            return False
#Module Exclusions
    def add_module_exclusion(self, ex):
        """Add a module to be excluded from all trace functions & methods"""
        assert type(ex) is str, "Exclusion {ex} is not string"
        self.moduleexclusions.append(ex)

    def delete_module_exclusion(self, ex):
        """Removes a module exclusion"""
        assert type(ex) is str, "Exclusion {ex} is not string"
        if ex in self.moduleexclusions:
            self.moduleexclusions.remove(ex)

    def module_excluded(self, ex):
        """Returns True if a module is to be excluded"""
        if ex in self.moduleexclusions:
            return True
        else:
            return False

    def start(self):
        """Starts tracing can be stopped by tracer.stop() or by setting sys.settrace(None)"""
        sys.settrace(tracerdespatcher)

    def stop(self):
        """Stops tracing"""
        sys.settrace(None)

def tracerdespatcher(frame, event, arg):
    """Despatcher function for the Tracer class"""
    frame.f_trace_opcodes = True
    if not tracer.function_excluded(frame.f_code.co_name) and not tracer.module_excluded(frame.f_code.co_filename):
        for func in tracer.functions:
            if not tracer.event_filter(func,event):
                func(frame, event, arg)
    return tracerdespatcher

class TracerClass():
    """Base class to inherit for implementing Tracer (essentially sys.settrace() with a class method)"""
    def __init__(self):
        """"""
        self.active=False

    def start(self):
        """Activate the trace note that tracer.start() must have been executed too"""
        self.active=True

    def stop(self):
        """Deactivate the trace"""
        self.active=False

    def trace(self, frame, event, arg):
        """The trace function (see sys.settrace() wrapped up as a method) overrid this to create your own trace"""
        if not self.active:
            return

tracer=Tracer()
