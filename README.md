# Tracer
Wrapper for Pythons sys.settrace

Allows you to run multiple traces at once and also allows you to queue up a class instead of the default show_trace() function.

## Example:
    from tracer import *
    import opcode
    def show_trace1(frame, event, arg):
        code = frame.f_code
        offset = frame.f_lasti

        print(f"Trace1| {event:10} | {str(arg):>4} |", end=' ')
        print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
        print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
        return show_trace1

    def show_trace2(frame, event, arg):
        code = frame.f_code
        offset = frame.f_lasti

        print(f"Trace2| {event:10} | {str(arg):>4} |", end=' ')
        print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
        print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
        return show_trace2

    class TClass(TracerClass):
        def trace(self, frame, event, arg):
            code = frame.f_code
            offset = frame.f_lasti
            print(f"Trace3| {event:10} | {str(arg):>4} |", end=' ')
            print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
            print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
            return self

    def fib(n):
        i, f1, f2 = 1, 1, 1
        while i < n:
            f1, f2 = f2, f1 + f2
            i += 1
        return f1

    tracer.add(show_trace1)
    tracer.add(show_trace2)
    tc=TClass()
    tracer.add(tc.trace)
    tc.start()
    tracer.start()
    fib(3)
    tracer.stop()
