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

class Atom:
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z

    def __str__(self):
        return f"Element: {self.atom.element}\n" +\
            f"x: {self.atom.x}\n" +\
            f"y: {self.atom.y}\n" +\
            f"z: {self.z}"


def main():
    x = 3.0

    c_atom = molecule.atom("H", x, 1.0, 4.0)
    atom = Atom(c_atom)

    string = str(atom)
    
    print(string)

if __name__ == "__main__":
    main()

