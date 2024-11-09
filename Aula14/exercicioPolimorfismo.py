"""     Crie uma classe pai com o nome FiguraGenerica.
Crie as classes Retangulo, Triangulo e Circulo que herdam de FiguraGenerica.
Defina o método __init__ para Retangulo, Triangulo e Circulo, passando os seguintes parâmetros: 
(altura e largura), (base e altura) e o (raio), respectivamente.  
Defina também o método calcular_area para todas as classes.
Para a classe FiguraGenerica o método calcular_area será declarado como vazio (pass). 
Para as outras classes Retangulo, Triangulo e Circulo, o método calcular_area retornará o cálculo de sua área respectiva.

Para finalizar crie uma lista com algumas instâncias das classes Retangulo, Triangulo e Circulo.
E, finalmente itere nesta lista imprimindo suas respectivas áreas."""

import math
from random import randint

class FiguraGenerica:
     def calcular_area(self):
          pass

class Retangulo(FiguraGenerica):
     def __init__(self, altura, largura):
          self.altura = int(altura)
          self.largura = int(largura)
     
     def calcular_area(self):
          return self.altura * self.largura

class Triangulo(FiguraGenerica):
     def __init__(self, base, altura):
          self.base = int(base)
          self.altura = int(altura)
     
     def calcular_area(self):
          return (self.altura * self.base) / 2

class Circulo(FiguraGenerica):
     def __init__(self,raio):
          self.raio = int(raio)

     def calcular_area(self):
          return f"{self.raio **2 *math.pi:.2f}"


a = randint(1,20)
b = randint(1,20)

figuras = [Retangulo(a,b), Triangulo(a,b), Circulo(a)]
for i in figuras:
     print(i.calcular_area())


