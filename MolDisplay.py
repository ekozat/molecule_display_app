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

    def __str__(self):
        return f"a1, a2: {self.bond.a1}, {self.bond.a2}\n" +\
            f"epairs: {self.bond.epairs}\n" +\
            f"x1, x2: {self.bond.x1}, {self.bond.x2}\n" +\
            f"y1, y2: {self.bond.y1}, {self.bond.y2}\n" +\
            f"z: {self.bond.z}\n" +\
            f"len: {self.bond.len}\n" +\
            f"dx, dy: {self.bond.dx}, {self.bond.dy}\n"

    def svg(self):
        
        ## Citation: TA helped correct calculations for bond structure ##

        # calculating proper pixel coords

        new_dx = self.bond.dx * 10.0
        new_dy = self.bond.dy * 10.0

        p1 = ((self.bond.x1 * 100.0) + offsetx) - new_dy
        p2 = ((self.bond.y1 * 100.0) + offsety) + new_dx
        
        p3 = ((self.bond.x1 * 100.0) + offsetx) + new_dy
        p4 = ((self.bond.y1 * 100.0) + offsety) - new_dx

        p5 = ((self.bond.x2 * 100) + offsetx) + new_dy
        p6 = ((self.bond.y2 * 100) + offsety) - new_dx
        
        p7 = ((self.bond.x2 * 100) + offsetx) - new_dy
        p8 = ((self.bond.y2 * 100) + offsety) + new_dx

        return f' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' %\
                (p1, p2, p3, p4, p5, p6, p7, p8)

class Molecule(molecule.molecule):
    def __str__(self):
        return f"atom_max, atom_no: {self.atom_max}, {self.atom_no}\n" +\
            f"bond_max, bond_no: {self.bond_max}, {self.bond_no}\n" +\
            f"atoms address: {id(self.atoms)}"

    # issue with sort function
    # Fixed: pop from the START
    def svg(self):
        # keep track of the number of elements in each array
        a_num = 0    #self.atom_no - 1 
        b_num = 0    #self.bond_no - 1

        # not self.atom_max because it is NOT how many atoms we have
        a_max = self.atom_no # -1 because of indexing (last element)
        b_max = self.bond_no

        arr = []

        # pop the first two comparisons
        a1 = self.get_atom(a_num)
        a1 = Atom(a1)

        b1 = self.get_bond(b_num)
        b1 = Bond(b1)

        # compare and cycle while bonds and atoms exist
        # while b_num >= 0 and a_num >= 0 
        while b_num < b_max and a_num < a_max: 
            print()
            print(f"a:{a1.z} vs. b:{b1.z}")
            if a1.z < b1.z:
                arr.append(a1.svg())

                # test #
                # print("Atom z is smaller than bond z")
                # print(a1.__str__())

                a_num += 1
                if a_num == a_max:
                    continue
                a1 = self.get_atom(a_num)
                a1 = Atom(a1)
                
            elif b1.z < a1.z:
                arr.append(b1.svg())

                # test #
                # print("Bond z is smaller than atom z")
                # print(b1.__str__())

                b_num += 1
                if b_num == b_max:
                    continue
                b1 = self.get_bond(b_num)
                b1 = Bond(b1)

            else:
                arr.append(a1.svg())
                arr.append(b1.svg())

                # test #
                # print("Equal")
                # print(a1.__str__())

                # test #
                # print("Equal")
                # print(b1.__str__())

                a_num += 1
                if a_num < a_max:
                    a1 = self.get_atom(a_num)
                    a1 = Atom(a1)

                b_num += 1
                if b_num < b_max:
                    b1 = self.get_bond(b_num)
                    b1 = Bond(b1)

        # once one array ends, append the rest of the atoms or bond
        while a_num < a_max:
            print(a_num)
            a1 = self.get_atom(a_num)
            a1 = Atom(a1)

            # test #
            # print("bonds are done")
            # print(a1.__str__())

            a_num += 1
            arr.append(a1.svg())
        while b_num < b_max:
            b1 = self.get_bond(b_num)
            b1 = Bond(b1)

            # test #
            # print("atoms are done")
            # print(b1.__str__())

            b_num += 1
            arr.append(b1.svg())

        # return statement
        return header + f"{arr}" + footer


    def parse(self, file):
        a_count = 0
        b_count = 0
        # if in bytes decode, if not treat as string

        # read first four lines
        for i in range(4):
            line = file.readline().decode()
            # if (isinstance(line, bytes) == True):
            #     line.decode()
            

        # read first two numbers
        a_count = int(line.strip().split()[0])
        b_count = int(line.strip().split()[1])

        # parse atoms
        for i in range(a_count):
            line = file.readline().decode("utf-8")

            x = float(line.strip().split()[0])
            y = float(line.strip().split()[1])
            z = float(line.strip().split()[2])
            element = line.strip().split()[3]

            self.append_atom(element, float(x), float(y), float(z))

        # parse bonds
        for i in range(b_count):
            line = file.readline().decode("utf-8")
            
            a1 = int(line.strip().split()[0]) 
            a2 = int(line.strip().split()[1])
            epairs = int(line.strip().split()[2])

            self.append_bond(a1, a2, epairs)


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

    ### molecule svg test (sort bonds + atoms) ###

    # molecule svg test
    # print(mol.__str__())
    # ret = mol.svg()
    # print(ret) - uncomment for first test

    # parse test
    # idk if we need to put some intial binary data
    mol2 = Molecule()
    file = open("CID_31260.sdf", "rb")
    # load input data into BytesIO
    text = io.TextIOWrapper(file)

    # the holy trinity
    mol2.parse(file)
    mol2.sort()
    # svg = mol2.svg()

    #ok it works

if __name__ == "__main__":
    main()
