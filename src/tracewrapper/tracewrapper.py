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
from pathlib import Path

class tracewrapper():
    """
    tracewrapper is a wrapper class for sys.settrace()
    """
    @staticmethod
    def __init__(_trace_lines=True, _trace_opcodes=False):
        """Initialise tracewrapper
           Parameters:
                _trace_lines boolean turns the trace lines event on default = True
                _trace_opcodes boolean turns the trace opcodes event on default = False
                """
        tracewrapper.functions=[]
        tracewrapper.functionexclusions=[]
        tracewrapper.moduleexclusions=[]
        tracewrapper.filters={}
        tracewrapper._trace_lines=_trace_lines
        tracewrapper._trace_opcodes=_trace_opcodes
        tracewrapper.add_module_exclusion("tracewrapper.py")

    @staticmethod
    def add(func):
        """Adds a tracer function (see sys.trace()) or the TracerClass.trace() method"""
        if isinstance(func, types.FunctionType):
            tracewrapper.functions.append(func)
            tracewrapper.add_function_exclusion(func.__name__)

        elif isinstance(func, types.MethodType):
            tracewrapper.functions.append(func)
            tracewrapper.add_function_exclusion(func.__name__)

        else:
            assert isinstance(func, FunctionType), "Passed function is not a function or a method"

    @staticmethod
    def delete( func):
        """"Removes a trace function"""
        if isinstance(func, types.FunctionType):
            tracewrapper.functions.remove(('func',func))
            tracewrapper.delete_function_exclusion(func.__name__)

        elif isinstance(func, types.MethodType):
            tracewrapper.functions.remove(('meth',func))
            tracewrapper.delete_function_exclusion(func.__name__)

#filters
    @staticmethod
    def add_event_filter( func, event):
        """Adds a filter to a trace function or method"""
        if func in tracewrapper.functions:
            if tracewrapper not in tracewrapper.filters:
                tracewrapper.filters[func]=list()
            tracewrapper.filters[func].append(event)
        else:
            assert func in tracewrapper.functions, "Cannot add filter for function that hasn't been added"

    @staticmethod
    def delete_event_filter(func, event):
        """Removes a trace filter"""
        if func in tracewrapper.functions:
            if func not in tracewrapper.filters:
                tracewrapper.filters[func]=list()
            if event in self.filters[func]:
                tracewrapper.filters[func].remove(event)
        else:
            assert func in tracewrapper.functions, "Cannot delete filter from function that hasn't been added"

    #returns true if filter is active
    @staticmethod
    def event_filter(func, event):
        """Returns True if the event for this function is being filtered"""
        assert func in tracewrapper.functions, "Cannot filter for function that hasn't been added"
        if func not in tracewrapper.filters:
            return False
        if event not in tracewrapper.filters[func]:
            return False
        return True


#Function Exclusions
    @staticmethod
    def add_function_exclusion(ex):
        """Add a function to exclude from all trace functions or methods"""
        assert isinstance(ex, str), "Exclusion {ex} is not string"
        tracewrapper.functionexclusions.append(ex)

    @staticmethod
    def delete_function_exclusion(ex):
        """Remove a function exclusion"""
        assert isinstance(ex, str), "Exclusion {ex} is not string"
        if ex in tracewrapper.functionexclusions:
            tracewrapper.functionexclusions.remove(ex)

    @staticmethod
    def function_excluded(ex):
        """Returns True if function is excluded"""
        return bool(ex in tracewrapper.functionexclusions)

#Module Exclusions
    @staticmethod
    def add_module_exclusion(ex):
        """Add a module to be excluded from all trace functions & methods"""
        assert isinstance(ex, str), "Exclusion {ex} is not string"
        tracewrapper.moduleexclusions.append(ex)

    @staticmethod
    def delete_module_exclusion(ex):
        """Removes a module exclusion"""
        assert isinstance(ex, str), "Exclusion {ex} is not string"
        if ex in tracewrapper.moduleexclusions:
            tracewrapper.moduleexclusions.remove(ex)

    @staticmethod
    def module_excluded(ex):
        """Returns True if a module is to be excluded"""
        return bool(Path(ex).name in tracewrapper.moduleexclusions)

    @staticmethod
    def start():
        """Starts tracing can be stopped by tracewrapper.stop() or by setting sys.settrace(None)"""
        sys.settrace(tracewrapper.tracerdespatcher)

    @staticmethod
    def stop():
        """Stops tracing"""
        sys.settrace(None)

    @staticmethod
    def tracerdespatcher(frame, event, arg):
        """Despatcher for the Tracer class"""
        frame.f_trace_opcodes = tracewrapper._trace_opcodes
        frame.f_trace_lines = tracewrapper._trace_lines
        if not tracewrapper.function_excluded(frame.f_code.co_name) and not tracewrapper.module_excluded(frame.f_code.co_filename):
            for func in tracewrapper.functions:
                if not tracewrapper.event_filter(func,event):
                    func(frame, event, arg)

        return tracewrapper.tracerdespatcher

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
