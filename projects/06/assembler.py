import sys

class Assembler:
    def __init__(self, fn):
        self.fn = fn
        self.symbols = dict()

        for i in range(16):
            self.symbols['R{}'.format(i)] = i
        self.symbols['SCREEN'] = 16384
        self.symbols['KBD'] = 24576
        self.symbols['SP'] = 0
        self.symbols['LCL'] = 1
        self.symbols['ARG'] = 2
        self.symbols['THIS'] = 3
        self.symbols['THAT'] = 4

        self.content = []
        self.result = []

    def translate_a_instruction(self, v):
        decimal = int(v)
        real_str =  bin(decimal)[2:]
        return '0' * (16 - len(real_str)) + real_str

    def translate_a_part(self, comp):
        if 'M' in comp:
            return '1'
        return '0'

    def translate_dest(self, dest):
        result = ['0', '0', '0']
        if 'M' in dest:
            result[-1] = '1'
        if 'D' in dest:
            result[-2] = '1'
        if 'A' in dest:
            result[-3] = '1'
        return ''.join(result)

    def translate_comp(self, comp):
        d = dict()
        d['0'] = '101010'
        d['1'] = '111111'
        d['-1'] = '111010'
        d['D'] = '001100'
        d['A'] = '110000'
        d['M'] = '110000'
        d['!D'] = '001101'
        d['!A'] = '110001'
        d['!M'] = '110001'
        d['-D'] = '001111'
        d['-A'] = '110011'
        d['-M'] = '110011'
        d['D+1'] = '011111'
        d['A+1'] = '110111'
        d['M+1'] = '110111'
        d['D-1'] = '001110'
        d['A-1'] = '110010'
        d['M-1'] = '110010'
        d['D+A'] = '000010'
        d['D+M'] = '000010'
        d['D-A'] = '010011'
        d['D-M'] = '010011'
        d['A-D'] = '000111'
        d['M-D'] = '000111'
        d['D&A'] = '000000'
        d['D&M'] = '000000'
        d['D|A'] = '010101'
        d['D|M'] = '010101'

        d['1+D'] = '011111'
        d['1+A'] = '110111'
        d['1+M'] = '110111'
        d['A+D'] = '000010'
        d['M+D'] = '000010'
        d['A&D'] = '000000'
        d['M&D'] = '000000'
        d['A|D'] = '010101'
        d['M|D'] = '010101'

        c_list = comp.split()
        c = ''.join(c_list)
        return d[c]

    def translate_jump(self, jump):
        d = dict()
        d[''] = '000'
        d['JGT'] = '001'
        d['JEQ'] = '010'
        d['JGE'] = '011'
        d['JLT'] = '100'
        d['JNE'] = '101'
        d['JLE'] = '110'
        d['JMP'] = '111'
        return d[jump]

    def translate_c_instruction(self, c):
        c_split_semicolon = c.split(';')
        dest_comp = c_split_semicolon[0].strip()
        dest_comp_split = dest_comp.split('=')
        comp_part = dest_comp_split[-1].strip()

        a = self.translate_a_part(comp_part)
        comp = self.translate_comp(comp_part)

        dest_part = ''
        if len(dest_comp_split) == 2:
            dest_part = dest_comp_split[-2].strip()
        dest = self.translate_dest(dest_part)

        jump_part = ''
        if len(c_split_semicolon) == 2:
            jump_part = c_split_semicolon[1].strip()
        jump = self.translate_jump(jump_part)

        return '111{}{}{}{}'.format(a, comp, dest, jump)


    def input(self):
        with open(self.fn, 'r') as f:
            for line in f.readlines():
                self.content.append(line.strip('\n').strip())

    def omit_blank_linses_and_comments(self):
        result = []
        for line in self.content:
            new_line = line
            if '/' in line:
                idx = line.index('/')
                new_line = new_line[:idx]
            new_line = new_line.strip()
            if new_line == '':
                continue
            result.append(new_line)
        self.result = result


    def sweep_label(self):
        result = []
        idx = 0
        for line in self.result:
            if '(' in line:
                self.symbols[line[1:-1]] = idx
                continue
            idx += 1
            result.append(line)
        self.result = result

    def sweep_symbol(self):
        n = 16
        result = []
        for line in self.result:
            if '@' in line:
                v = line[1:]
                try:
                    int(v)
                    result.append(self.translate_a_instruction(v))
                except:
                    if v in self.symbols:
                        result.append(self.translate_a_instruction(self.symbols[v]))
                    else:
                        result.append(self.translate_a_instruction(n))
                        self.symbols[v] = n
                        n += 1
            else:
                result.append(self.translate_c_instruction(line))
        self.result = result

    def deal(self):
        self.input()
        self.omit_blank_linses_and_comments()
        self.sweep_label()
        self.sweep_symbol()

    def output(self):
        with open(self.fn[:-4] + '.hack', 'w') as f:
            for i in self.result:
                f.write(i)
                f.write('\n')

if __name__ == '__main__':
    fn = sys.argv[1]
    assembler = Assembler(fn)
    assembler.deal()
    assembler.output()
