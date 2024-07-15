import sys
from typing import Dict, List


def parse(line: str):
    parts = (
        line.replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("X", "")
        .replace("#", "")
        .replace("ZR", "31")
        .split()
    )

    return [parts[0]] + list(map(int, parts[1:]))


def convert_instruction_to_int(tokens, OPCODE_MAP: Dict[str, int]) -> int:

    instruction = tokens[0]
    if instruction not in OPCODE_MAP:
        raise SyntaxError(f"Invalid Command: {tokens}")

    num: int = OPCODE_MAP[instruction]

    if instruction == "B":
        return num | (tokens[1]) & 0x3FFFFFF
    elif instruction in ["CBZ", "CBNZ"]:
        return num | ((tokens[2]) & 0x7FFFF) << 5 | tokens[1]
    elif instruction in ["ADD", "SUB"]:
        return num | (tokens[1]) << 16 | (tokens[2]) << 5 | tokens[3]
    elif instruction in ["ADDI", "SUBI"]:
        return num | (tokens[3]) << 10 | (tokens[2]) << 5 | tokens[1]
    elif instruction in ["STUR", "LDUR"]:
        return num | ((tokens[3]) & 0x1FF) << 10 | (tokens[2]) << 5 | tokens[1]
    else:
        raise SyntaxError(f"Unhandled instruction: {instruction}")
