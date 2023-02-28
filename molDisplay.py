import molecule
import io

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
        
        # calculating proper pixel coords
        new_x1 = self.bond.x1 * 100.0 + offsetx
        new_x2 = self.bond.y1 * 100.0 + offsety
        new_y1 = self.bond.x2 * 100.0 + offsetx
        new_y2 = self.bond.y2 * 100.0 + offsetx

        new_dx = self.bond.dx * 10.0
        new_dy = self.bond.dy * 10.0

        # make sure drawing in the correct order
        # offset of atom1
        x1 = new_x1 - new_dy
        y1 = new_y1 - new_dx
        x2 = new_x1 + new_dy
        y2 = new_y1 + new_dx

        # offset of atom2
        x3 = new_x2 + new_dy
        y3 = new_y2 + new_dx
        x4 = new_x2 - new_dy
        y4 = new_y2 - new_dx

        return f' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' %\
                (x1, y1, x2, y2, x3, y3, x4, y4)

class Molecule(molecule.molecule):
    def __str__(self):
        return f"atom_max, atom_no: {self.atom_max}, {self.atom_no}\n" +\
            f"bond_max, bond_no: {self.atom_max}, {self.atom_no}\n" +\
            f"atoms address: {id(self.atoms)}"

    def svg(self):
        #keep track of the number of elements in each array
        a_num = self.atom_no - 1 # -1 because of indexing
        b_num = self.bond_no - 1

        arr = []
        print(a_num) # test
        print(b_num) # test

        # pop the first two comparisons
        a1 = self.get_atom(a_num)#self.atoms.pop(a_num) #so not pop
        # a_num -= 1
        a1 = Atom(a1)

        b1 = self.get_bond(b_num)#self.bonds.pop(b_num)
        # b_num -= 1
        b1 = Bond(b1)

        print(a1.z)

        # compare and cycle
        # this might not work but it seems like it will
        while b_num >= 0 or a_num >= 0: 
            print("loop") #test

            if a1.z < b1.z:
                print("atom") #test

                arr.append(a1.svg())
                print(a1.__str__() + '\n')

                # if the atoms are done, start comparing bonds against bonds
                if a_num < 0 and b_num >= 0:
                    a1 = self.get_bond(b_num)#self.bonds.pop(b_num)
                    b_num -= 1
                    a1 = Bond(a1)
                else:
                    a1 = self.get_atom(a_num)
                    a_num -= 1
                    a1 = Atom(a1)

            elif b1.z < a1.z:
                print("bond") #test

                arr.append(b1.svg())
                print(b1.__str__() + '\n')

                print(a_num) # test
                print(b_num) # test

                # if the bonds are sorted first, start comparing atoms against atoms
                if b_num < 0 and a_num >= 0:
                    b1 = self.get_atom(a_num)
                    a_num -= 1
                    b1 = Atom(b1)

                else:
                    b1 = self.get_bond(b_num)
                    b_num -= 1
                    b1 = Bond(b1)

        print(a_num) # test
        print(b_num) # test

        # return statement
        return header + f"{arr}" + footer




    # def parse(self, file):




def main():
    ### atom testing ###
    x = 3.0

    c_atom = molecule.atom("H", x, 1.0, 4.0)
    atom = Atom(c_atom)

    #string = atom.str()
    #string2 = atom.svg()
    #print(string2)

    ### bond testing ###
    mol = Molecule() # molecule.molecule() - creates a new molecule object
    mol.append_atom("O", 2.5369, -0.1550, 1.5000)
    mol.append_atom("H", 3.0739, 0.1550, 1.0000)
    mol.append_bond(1, 2, 1)

    c_bond = mol.get_bond(0)
    bond = Bond(c_bond)

    string = bond.svg()
    # print(string)

    # atom = mol.get_atom(0)
    # print(atom.x)

    # molecule svg test
    # mol = Molecule()
    print(mol.__str__())
    ret = mol.svg()
    print(ret)

    # parse test
    # idk if we need to put some intial binary data
    #file = open("CIS")
    # load input data into BytesIO
    #text = io.TextIOWrapper(file)

    #for line in text:
    #    print(line)

if __name__ == "__main__":
    main()

