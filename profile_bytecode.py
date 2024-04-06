import sys
import dis

# Initialize a dictionary to count opcodes
opcode_counts = {opname: 0 for opname in dis.opname}


def trace(frame, event, arg):
    if event == 'call':
        # Get bytecode for the current frame
        code_obj = frame.f_code
        bytecode = code_obj.co_code

        # Iterate through bytecode instructions
        for offset in range(0, len(bytecode), 2):
            opcode = bytecode[offset]
            opcode_counts[dis.opname[opcode]] += 1
    return trace


# Set the trace function
sys.settrace(trace)

# Example function to profile


def example():
    a = 1
    b = 2
    c = a + b
    print(c)


example()

# Reset trace to None to stop tracing
sys.settrace(None)

# Print opcode counts
for opcode, count in opcode_counts.items():
    if count > 0:
        print(f"{opcode}: {count}")
