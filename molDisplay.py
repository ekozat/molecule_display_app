import molecule

mol = molecule.molecule() #create new molecule object

radius ={   'H': 25,
            'C': 40,
            'O': 40,
            'N': 40,
        }

element_name = {'H': 'grey',
                'C': 'black',
                'O': 'red',
                'N': 'blue',
            }

header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500

b_pixel_offset = 10

class Atom:
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z

    def __str__(self):
        return f"Element: {self.atom.element}\n" +\
            f"x: {self.atom.x}\n" +\
            f"y: {self.atom.y}\n" +\
            f"z: {self.z}"

    def svg(self):
        new_x = self.atom.x * 100.0 + offsetx
        new_y = self.atom.y * 100.0 + offsety

        for r in radius:
            if self.atom.element == r:
                new_r = radius[r]

        for fill in radius:
            if self.atom.element == fill:
                new_fill = element_name[fill]

        return f'  <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n' % (new_x, new_y, new_r, new_fill)

class Bond:
    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = c_bond.z

    # how would I check all atoms array?
    # f"atom1: {self.bond.atoms[self.bond.a1]}\n" +\
    # f"atom2: {self.bond.atoms[self.bond.a2]}\n" +\
    def __str__(self):
        return f"a1, a2: {self.bond.a1}, {self.bond.a2}\n" +\
            f"epairs: {self.bond.epairs}\n" +\
            f"x1, x2: {self.bond.x1}, {self.bond.x2}\n" +\
            f"y1, y2: {self.bond.y1}, {self.bond.y2}\n" +\
            f"z: {self.bond.z}\n" +\
            f"len: {self.bond.len}\n" +\
            f"dx, dy: {self.bond.dx}, {self.bond.dy}\n"

    def svg(self):
        # offset of atom1
        x1 = self.bond.x1 - self.bond.dy*10.0
        y1 = self.bond.y1 - self.bond.dx*10.0
        x2 = self.bond.x1 + self.bond.dy*10.0
        y2 = self.bond.y1 + self.bond.dx*10.0

        # offset of atom2
        x3 = self.bond.x2 - self.bond.dy*10.0
        y3 = self.bond.y2 - self.bond.dx*10.0
        x4 = self.bond.x2 + self.bond.dy*10.0
        y4 = self.bond.y2 + self.bond.dx*10.0

        return f' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' %\
                (x1, y1, x2, y2, x3, y3, x4, y4)

def main():
    ### atom testing ###
    x = 3.0

    c_atom = molecule.atom("H", x, 1.0, 4.0)
    atom = Atom(c_atom)

    #string = atom.str()
    #string2 = atom.svg()
    #print(string2)

    ### bond testing ###
    mol = molecule.molecule()
    mol.append_atom("O", 2.5369, -0.1550, 0.0000)
    mol.append_atom("H", 3.0739, 0.1550, 0.0000)
    mol.append_bond(1, 2, 1)

    c_bond = mol.get_bond(0)
    bond = Bond(c_bond)

    string = bond.svg()
    print(string)

if __name__ == "__main__":
    main()

