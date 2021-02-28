from math import gcd

class Group:
    def __init__(self, elements, operation, table_name_map):
        """
        elements:       elements of the group
        operation:      operation on group
        table_name_map: map for cayley table to prettify any complex objects in groups for printing
        """
        self.elements = elements
        self.operation = operation
        self.table_name_map = table_name_map
        self.id = None #placeholder to find group identity later
    
    def compose(self, e1, e2):
        """
        e1: element 1 of composition
        e2: element 2 of composition
        returns the composition of e1 and e2. read "e1 o e2"
        """
        if (e1 not in self.elements) or (e2 not in self.elements):
            raise Exception('Elements not in group.')
        value = self.operation(e1, e2)
        if value not in self.elements:
            raise Exception('Closure does not hold for {0} + {1} = {2}.'.format(e1,e2,value))
        return value
        
    def identity(self):
        """
        Gets the identity of the group
        """
        if self.id:
            return self.id #if already found return
        for element in self.elements:
            for test_element in self.elements:
                if not (self.compose(element, test_element) == test_element):
                    break
            self.id = element
            return element
        #shouldn't reach
        raise Exception('No identity, not a group')

    def inverse(self, e):
        """
        e: element to find inverse of
        finds the inverse of an element `e`
        """
        for element in self.elements:
            if self.compose(e, element) == self.identity():
                return element
        #shouldn't reach
        raise Exception('No inverse for {0}, not a group'.format(e)) 

    def __repr__(self):
        longest = max(len(str(v)) for k,v in self.table_name_map.items()) + 2
        #makes an element into a guarenteed len cell
        def cell(data,filler=' '):
            #thanks https://stackoverflow.com/questions/5676646/how-can-i-fill-out-a-python-string-with-spaces
            return '{message:{fill}{align}{width}}'.format(
               message=data,
               fill=filler,
               align='^',
               width=longest
            )
        #maps elements to pretty values and strs
        def data_cell(e):
            return cell(str(self.table_name_map[e]))
        vert_sepr = '|' #vertical bar separator
        def hori_sepr(char): #horizontal row separator
            return cell('',filler=char)
        def row_sepr(char): #row separator
            return (hori_sepr(char) + vert_sepr * 2) + ((hori_sepr(char) + vert_sepr) * len(self.elements)) + '\n'

        cayley = cell('o') + vert_sepr * 2
        #headers
        for header in self.elements:
            cayley += data_cell(header) + vert_sepr
        cayley += '\n' + row_sepr('=')

        #table
        for row in self.elements:
            line = (data_cell(row) + vert_sepr * 2)
            for column in self.elements:
                line += data_cell(self.compose(row,column)) + vert_sepr
            cayley += line + '\n' + row_sepr('-')
        return cayley

"""def left_cosets(G, H):
            oG = len(G)
            oH = len(H)
            iGH = oG / oH
            GH = []
            for g in G:
                gHe = range(0, oH)
            for j in range(0, oH):
                gHe[j] = g * H[j]
            gH = coset(gHe)
            set_append_unique(GH, gH)
            return GH
"""
        



def coprime(a,b):
    return gcd(a,b) == 1
def U(n):
    elements = [e for e in range(1,n) if coprime(e,n)]
    return Group(elements, lambda e1, e2: ((e2 * e1) % n), {e : e for e in elements})


def Z(n):
    elements = [e for e in range(0,n)]
    return Group(elements, lambda e1, e2: ((e2 + e1) % n), {e : e for e in elements})

def is_closed(H,G):
    k=True
    if set(H).issubset(set(G.elements))==True:
        for a in list(H):
            if set([G.compose(a,b) for b in H]).issubset(set(H)) == False:
                k=False
    if set(H).issubset(set(G.elements))==False:
        k=False
    return k







def power_set(A):
    """A is an iterable (list, tuple, set, str, etc)
    returns a set which is the power set of A."""
    length = len(A)
    l = [a for a in A]
    ps = set()

    for i in range(2 ** length):
        selector = f'{i:0{length}b}'
        subset = {l[j] for j, bit in enumerate(selector) if bit == '1'}
        ps.add(frozenset(subset))

    return [set(i) for i in ps]

def Subgrupos(G):
    sub= []
    for i in power_set(G.elements):
        if len(i)>0:
            if is_closed(i,G) == True:
                sub.append(i)
    return sub
def superconjuntos(H , G):
    sp = []
    for i in Subgrupos(G):
        if H.issubset(i):
            sp.append(list(i))
    return sp
