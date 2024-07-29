import json
from time import sleep

# Debugging utilities

# List of breakpoints (addresses where execution will pause)
breakpoints = []

# Function to set a breakpoint
def set_breakpoint(address):
    if address not in breakpoints:
        breakpoints.append(address)
        print(f"Breakpoint set at 0x{address:04X}")
    else:
        print(f"Breakpoint already exists at 0x{address:04X}")

# Function to check if the current address is a breakpoint
def check_breakpoint(address):
    if address in breakpoints:
        print(f"Breakpoint hit at 0x{address:04X}")
        return True
    return False

# Enable or disable tracing
trace_enabled = True

def log_trace(opcode, pc, ac, ix, iy, sr, sp):
    if trace_enabled:
        print(f"TRACE: PC: 0x{pc:04X}, Opcode: {opcode}, AC: 0x{ac:02X}, X: 0x{ix:02X}, Y: 0x{iy:02X}, SR: {sr}, SP: 0x{sp:02X}")

# Load addrSet and insSet from JSON files
with open('addrSet.json') as f:
    addrSet = json.load(f)

with open('insSet.json') as f:
    insSet = json.load(f)

def AddrType(operand):
    abstracted_operand = ''.join('n' if c in "123456789ABCDEF" else c for c in operand)
    print(" [] - Operand abstracted as: " + abstracted_operand)
    if abstracted_operand in addrSet:
        print(" [] - Addressing Type match: " + addrSet[abstracted_operand])
        return addrSet[abstracted_operand]
    print("\n! Incorrect Addressing Type format: " + operand)
    return 0

def Exec():
    code = ""
    i = 0
    while i < len(insList):
        sleep(.15)

        if insList[i] not in insSet:
            print("\n! Unsupported Operation at i == " + str(i) + ": " + insList[i])
            return 0

        # Check for breakpoints
        if check_breakpoint(i):
            print("Execution paused at breakpoint.")
            input("Press Enter to continue...")

        # Fetch and execute the instruction
        opcode = insSet[insList[i]]
        pc = i  # Assume PC is the index for simplicity
        ac = AC  # Current Accumulator value
        ix = IX  # Index Register X value
        iy = IY  # Index Register Y value
        sr = SR  # Status Register value
        sp = SP  # Stack Pointer value

        # Log the trace
        log_trace(opcode, pc, ac, ix, iy, sr, sp)

        # Existing logic to handle instructions...
        # (Your current code here)

        i += 1


    print("\nFinal Assembled Code:")
    print(code)

# Example usage
insList = ["LDA", "#$01", "STA", "$0200", "LDX", "#$08", "STX", "$0001", "LDY", "#$FF", "STY", "$0201"]
Exec()
