import json
from time import sleep

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
        instruction = insList[i]
        if instruction not in insSet:
            print("\n! Unsupported Operation at i == " + str(i) + ": " + instruction)
            return 0

        print(f"\nAssembling at i == {i}: {instruction}")

        if instruction not in ["BRK", "CLC", "CLD", "CLI", "CLV", "DEX", "DEY", "INX", "INY", "NOP", "PHA", "PHP", "PLA", "PLP",
                               "RTI", "RTS", "SEC", "SED", "SEI", "TAX", "TAY", "TSX", "TXA", "TXS", "TYA", "EXT"]:
            addrType = "rel" if instruction in ["BCC", "BCS", "BEQ", "BMI", "BNE", "BPL", "BVC", "BVS"] else AddrType(insList[i + 1])
            try:
                opcode = insSet[instruction][addrType]
            except KeyError:
                print("\n! Non-compatible Addressing Type at i == " + str(i) + ": " + instruction)
                return 0

            print(f" - Addressing type == {addrType} and opcode == {opcode}")

            if addrType in ["imm", "zer", "x-zer", "y-zer", "x-zer-ind", "y-zer-ind"]:
                code += f"0x{opcode}, 0x{insList[i + 1][2:4]}, "
                print(f" -> 0x{opcode}, 0x{insList[i + 1][2:4]}, ")
                i += 1
            elif addrType in ["abs", "x-abs", "y-abs"]:
                code += f"0x{opcode}, 0x{insList[i + 1][3:5]}, 0x{insList[i + 1][1:3]}, "
                print(f" -> 0x{opcode}, 0x{insList[i + 1][3:5]}, 0x{insList[i + 1][1:3]}, ")
                i += 1
            elif addrType == "abs-ind":
                code += f"0x{opcode}, 0x{insList[i + 1][4:6]}, 0x{insList[i + 1][2:4]}, 0x{insList[i + 1][1:2]}, "
                print(f" -> 0x{opcode}, 0x{insList[i + 1][4:6]}, 0x{insList[i + 1][2:4]}, 0x{insList[i + 1][1:2]}, ")
                i += 1
            elif addrType == "rel":
                code += f"0x{opcode}, 0x{insList[i + 1]}, "
                print(f" -> 0x{opcode}, 0x{insList[i + 1]}, ")
                i += 1
            else:
                code += f"0x{opcode}, "
                print(f" -> 0x{opcode}, ")
        else:
            opcode = insSet[instruction]["imp"]
            print(f" - Implied addressing opcode == {opcode}")
            code += f"0x{opcode}, "

        i += 1

    print("\nFinal Assembled Code:")
    print(code)

# Example usage
insList = ["LDA", "#$01", "STA", "$0200", "LDX", "#$08", "STX", "$0001", "LDY", "#$FF", "STY", "$0201"]
Exec()
