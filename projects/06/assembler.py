import argparse


class Assembler:
    def __init__(self, fn):
        self.fn = fn

        self.raw_lines = []
        self.cleaned_lines = []
        self.label_lines = []
        self.result_lines = []

        self.symbols = dict()
        self.register_dict = dict()
        self.jump_dict = dict()

        self.init_symbol_data()
        self.init_register_data()
        self.init_jump_data()

    def init_symbol_data(self):
        for i in range(16):
            self.symbols["R{}".format(i)] = i
        self.symbols["SCREEN"] = 0x4000
        self.symbols["KBD"] = 0x6000
        self.symbols["SP"] = 0
        self.symbols["LCL"] = 1
        self.symbols["ARG"] = 2
        self.symbols["THIS"] = 3
        self.symbols["THAT"] = 4

    def init_jump_data(self):
        self.jump_dict[""] = "000"
        self.jump_dict["JGT"] = "001"
        self.jump_dict["JEQ"] = "010"
        self.jump_dict["JGE"] = "011"
        self.jump_dict["JLT"] = "100"
        self.jump_dict["JNE"] = "101"
        self.jump_dict["JLE"] = "110"
        self.jump_dict["JMP"] = "111"

    def init_register_data(self):
        self.register_dict["0"] = "101010"
        self.register_dict["1"] = "111111"
        self.register_dict["-1"] = "111010"
        self.register_dict["D"] = "001100"
        self.register_dict["A"] = "110000"
        self.register_dict["M"] = "110000"
        self.register_dict["!D"] = "001101"
        self.register_dict["!A"] = "110001"
        self.register_dict["!M"] = "110001"
        self.register_dict["-D"] = "001111"
        self.register_dict["-A"] = "110011"
        self.register_dict["-M"] = "110011"
        self.register_dict["D+1"] = "011111"
        self.register_dict["A+1"] = "110111"
        self.register_dict["M+1"] = "110111"
        self.register_dict["D-1"] = "001110"
        self.register_dict["A-1"] = "110010"
        self.register_dict["M-1"] = "110010"
        self.register_dict["D+A"] = "000010"
        self.register_dict["D+M"] = "000010"
        self.register_dict["D-A"] = "010011"
        self.register_dict["D-M"] = "010011"
        self.register_dict["A-D"] = "000111"
        self.register_dict["M-D"] = "000111"
        self.register_dict["D&A"] = "000000"
        self.register_dict["D&M"] = "000000"
        self.register_dict["D|A"] = "010101"
        self.register_dict["D|M"] = "010101"

        self.register_dict["1+D"] = "011111"
        self.register_dict["1+A"] = "110111"
        self.register_dict["1+M"] = "110111"
        self.register_dict["A+D"] = "000010"
        self.register_dict["M+D"] = "000010"
        self.register_dict["A&D"] = "000000"
        self.register_dict["M&D"] = "000000"
        self.register_dict["A|D"] = "010101"
        self.register_dict["M|D"] = "010101"

    def translate_a_instruction(self, v):
        return bin(int(v))[2:].zfill(16)

    def translate_a_part(self, comp):
        if "M" in comp:
            return "1"
        return "0"

    def translate_dest(self, dest):
        result = ["0", "0", "0"]
        if "A" in dest:
            result[0] = "1"
        if "D" in dest:
            result[1] = "1"
        if "M" in dest:
            result[2] = "1"
        return "".join(result)

    def translate_comp(self, comp):
        c_list = comp.split()
        c = "".join(c_list)
        return self.register_dict[c]

    def translate_jump(self, jump):
        return self.jump_dict[jump]

    def translate_c_instruction(self, c):
        c_split_semicolon = c.split(";")
        dest_comp = c_split_semicolon[0].strip()
        dest_comp_split = dest_comp.split("=")
        comp_part = dest_comp_split[-1].strip()

        a = self.translate_a_part(comp_part)
        comp = self.translate_comp(comp_part)

        dest_part = ""
        if len(dest_comp_split) == 2:
            dest_part = dest_comp_split[0].strip()
        dest = self.translate_dest(dest_part)

        jump_part = ""
        if len(c_split_semicolon) == 2:
            jump_part = c_split_semicolon[1].strip()
        jump = self.translate_jump(jump_part)

        return "111{}{}{}{}".format(a, comp, dest, jump)

    def input(self):
        with open(self.fn, "r") as f:
            for line in f.readlines():
                self.raw_lines.append(line.strip("\n").strip())

    def omit_blank_linses_and_comments(self):
        result = []
        for line in self.raw_lines:
            new_line = line
            if "/" in line:
                idx = line.index("/")
                new_line = new_line[:idx]
            new_line = new_line.strip()
            if new_line == "":
                continue
            result.append(new_line)
        self.cleaned_lines = result

    def sweep_label(self):
        result = []
        idx = 0
        for line in self.cleaned_lines:
            if line[0] == "(":
                self.symbols[line[1:-1]] = idx
                continue
            idx += 1
            result.append(line)
        self.label_lines = result

    def sweep_symbol(self):
        n = 16
        result = []
        for line in self.label_lines:
            if line[0] == "@":
                v = line[1:]
                raw_a_instruction = None
                if v.isdigit():
                    raw_a_instruction = v
                elif v in self.symbols:
                    raw_a_instruction = self.symbols[v]
                else:
                    raw_a_instruction = n
                    self.symbols[v] = n
                    n += 1

                result.append(self.translate_a_instruction(raw_a_instruction))
            else:
                result.append(self.translate_c_instruction(line))
        self.result_lines = result

    def deal(self):
        self.input()
        self.omit_blank_linses_and_comments()
        self.sweep_label()
        self.sweep_symbol()
        self.output()

    def output(self):
        with open(self.fn[:-4] + ".hack", "w") as f:
            for i in self.result_lines:
                f.write("{}\n".format(i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("assembler")
    parser.add_argument("-fn", help="assemble code file path", required=True)

    args = parser.parse_args()

    assembler = Assembler(args.fn)
    assembler.deal()
