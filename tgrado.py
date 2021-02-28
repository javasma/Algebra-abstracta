#!/usr/bin/env python
# coding: utf-8
import time
import numpy as np
import math
from math import gcd
from sympy import *
import sympy

class Group:
    def __init__(self, defn, elements, operation, table_name_map):
        """
        elements:       elements of the group
        operation:      operation on group
        table_name_map: map for cayley table to prettify any complex objects in groups for printing
        """
        self.defn = defn
        self.elements = elements
        self.operation = operation
        self.table_name_map = table_name_map
        self.id = None  # placeholder to find group identity later
        self.chi = lambda x: exp(2 * I * pi / len(self.elements))

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
            raise Exception('Closure does not hold for {0} + {1} = {2}.'.format(e1, e2, value))
        return value

    def identity(self):
        """
        Gets the identity of the group
        """
        if self.id:
            return self.id  # if already found return
        for element in self.elements:
            for test_element in self.elements:
                if not (self.compose(element, test_element) == test_element):
                    break
            self.id = element
            return element
        # shouldn't reach
        raise Exception('No identity, not a group')

    def inverse(self, e):
        """
        e: element to find inverse of
        finds the inverse of an element `e`
        """
        for element in self.elements:
            if self.compose(e, element) == self.identity():
                return element
        raise Exception('No inverse for {0}, not a group'.format(e))

    # ------------------------------------------------------------------------

    def order(self, e):
        element = e
        for i in range(len(self.elements)):
            if element == self.identity():
                break
            else:
                element = self.compose(element, e)
        return i + 1

    def orden(self):
        ordenes = [self.order(e) for e in self.elements]
        return ordenes

    def describe(self):
        print('Grupo de orden:', len(self.elements))
        if len(self.elements) in self.orden():
            print("El grupo es cíclico")
            print("Un generador pequeño es:", self.generadores()[0])
        else:
            print("El grupo no es cíclico")
        return np.array([self.elements, self.orden()])

    def generado(self, e):
        gen = []
        temp = e
        for i in range(1, self.order(e) + 1):
            gen = gen + [temp]
            temp = self.compose(temp, e)
        return gen

    def gen(self, e1, e2):
        temp = []
        mod = self.defn
        for i in self.generado(e1):
            for j in self.generado(e2):
                temp = temp + [(i * j) % mod]
        temp.sort()
        return temp

    def generadores(self):
        temp = []
        for e in self.elements:
            if self.order(e) == len(self.elements):
                temp = temp + [e]
        return temp

    # ----------------------------------------------------- MORFISMOS
    def Xi(self, n):
        matrix = []
        for i in range(1, len(self.elements) + 1):
            temp = [((self.generadores()[0] ** i) % self.defn), (self.chi(self.generadores()[0]) ** (i * n))]
            matrix = matrix + [temp]
        return matrix

    # ------------------------
    def omega(self, n):
        matrix = self.Xi(n)
        for i in range(0, len(matrix)):
            matrix[i] = np.prod(matrix[i])
        om = -np.sum(matrix)/(2*self.defn)
        return om


# ----------------------------------------------------------
def __repr__(self):
    longest = max(len(str(v)) for k, v in self.table_name_map.items()) + 2

    # makes an element into a guarenteed len cell
    def cell(data, filler=' '):
        # thanks https://stackoverflow.com/questions/5676646/how-can-i-fill-out-a-python-string-with-spaces
        return '{message:{fill}{align}{width}}'.format(
            message=data,
            fill=filler,
            align='^',
            width=longest
        )

    # maps elements to pretty values and strs
    def data_cell(e):
        return cell(str(self.table_name_map[e]))

    vert_sepr = '|'  # vertical bar separator

    def hori_sepr(char):  # horizontal row separator
        return cell('', filler=char)

    def row_sepr(char):  # row separator
        return (hori_sepr(char) + vert_sepr * 2) + ((hori_sepr(char) + vert_sepr) * len(self.elements)) + '\n'

    cayley = cell('o') + vert_sepr * 2
    # headers
    for header in self.elements:
        cayley += data_cell(header) + vert_sepr
    cayley += '\n' + row_sepr('=')

    # table
    for row in self.elements:
        line = (data_cell(row) + vert_sepr * 2)
        for column in self.elements:
            line += data_cell(self.compose(row, column)) + vert_sepr
        cayley += line + '\n' + row_sepr('-')
    return cayley


def coprime(a, b):
    return gcd(a, b) == 1


def U(n):
    defn = n
    elements = [e for e in range(1, n) if coprime(e, n)]
    return Group(defn, elements, lambda e1, e2: ((e2 * e1) % n), {e: e for e in elements})


def Z(n):
    defn = n
    elements = [e for e in range(0, n)]
    return Group(defn, elements, lambda e1, e2: ((e2 + e1) % n), {e: e for e in elements})


# ---------------- Lo más importante es esta función ----------------------------------------------------------------------------
def classno(p, m):
    init = time.time()
    G = U(p ** (m + 1))
    lol = 2 * G.defn
    ome = []
    for i in range(0, int(len(G.elements) / 2)):
        k = (2 * i) + 1
        ome = ome + [G.omega(k)]
    l = complex(np.prod(ome) * lol)
    numclass = round(re(l))
    t = time.time() - init
    if round(im(l)) == 0:
        print('Para el Cuerpo ciclotómico de orden', G.defn, ' El segundo factor es: ', numclass)
        print("El tiempo de computo es" "--- %s seconds ---" % t)
    return numclass, t

# In[ ]:
