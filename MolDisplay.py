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

    # issue with sort function
    def svg(self):
        #keep track of the number of elements in each array
        a_num = self.atom_no - 1 # -1 because of indexing
        b_num = self.bond_no - 1

        arr = []

        # pop the first two comparisons
        a1 = self.get_atom(a_num)
        a1 = Atom(a1)

        b1 = self.get_bond(b_num)
        b1 = Bond(b1)

        # compare and cycle while bonds and atoms exist
        while b_num >= 0 and a_num >= 0: 

            if a1.z < b1.z:
                arr.append(a1.svg())

                a_num -= 1
                if a_num == -1:
                    continue
                a1 = self.get_atom(a_num)
                a1 = Atom(a1)

            elif b1.z < a1.z:
                arr.append(b1.svg())

                b_num -= 1
                if b_num == -1:
                    continue
                b1 = self.get_bond(b_num)
                b1 = Bond(b1)
            else:
                arr.append(a1.svg())
                arr.append(b1.svg())

                a_num -= 1
                if a_num >= 0:
                    a1 = self.get_atom(a_num)
                    a1 = Atom(a1)

                b_num -= 1
                if b_num >= 0:
                    b1 = self.get_bond(b_num)
                    b1 = Bond(b1)

        # once one array ends, append the rest of the atoms or bond
        while a_num >= 0:
            a1 = self.get_atom(a_num)
            a1 = Atom(a1)
            a_num -= 1
            arr.append(a1.svg())
        while b_num >= 0:
            b1 = self.get_bond(b_num)
            b1 = Bond(b1)
            b_num -= 1
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
            line = file.readline()

            x = float(line.strip().split()[0])
            y = float(line.strip().split()[1])
            z = float(line.strip().split()[2])
            element = line.strip().split()[3].decode("utf-8") 

            self.append_atom(element, float(x), float(y), float(z))

        # parse bonds
        for i in range(b_count):
            line = file.readline()
            
            a1 = int(line.strip().split()[0]) 
            a2 = int(line.strip().split()[1])
            epairs = int(line.strip().split()[1])

            self.append_bond(a1, a2, epairs)