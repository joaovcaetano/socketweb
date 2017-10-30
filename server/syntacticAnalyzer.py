#-*- coding: utf-8 -*-

#comentarios (LINHA ): 15,37,28,35
from lexicAnalyzer_v1 import *
global o,aux

class Syntatic_analyzer(object):
    def __init__(self, pai) :
      self.pai = pai
    def __init__(self, pai,filhos=[],valor=0,lexema='') :
      self.pai = pai
      self.filhos  = filhos
      self.lexema = lexema #SE REFERE AOS ID E É USADO PARA BUSCAR A ENTRADA DA TABELA DAQUELE ID
      self.valor = valor #SERÁ USADO PELO INTERPRETADOR PARA GUARDAR O VALOR DE TODAS AS EXPRESSOES
      #self.tipo = tipo #PROXIMO TP

    def __str__(self) :
      return str(self.pai)
    def getNumber(self,filhos,tokk):
      x=filhos[0]
      if x is not tokk:
          return None
      return o.token[0]
    def match(self,tokk):
        if(tokk == o.T[0]):
            o.T.pop(0)
            o.token.pop(0)

            print 'Esta entrada é esperada'
        else:
            #PRINTO OQ ESTOU COMPARANDO SÓ PARA TESTAR
            print 'Token '+o.T[0]
            print 'TOken esperado: '+tokk
            print 'Erro sintático, entrada nao esperada'

    def Programa(self):
        print 'Programa'
        self.match('INT')
        self.match('MAIN')
        self.match('LBRACKET')
        self.match('RBRACKET')
        self.match('LBRACE')
        programa = Syntatic_analyzer('Programa',[])
        programa.filhos.append(self.Decl_Comando())
        self.match('RBRACE')
        return programa
    def Decl_Comando(self):
        print 'Decl_Comando'
        if(o.T[0] == 'INT' or o.T[0] == 'FLOAT'):
            TOP= Syntatic_analyzer('Decl_Comando',[])
            TOP.filhos.append(self.Declaracoes())
            TOP.filhos.append(self.Decl_Comando())
            return TOP
        elif(o.T[0] == 'LBRACE') or (o.T[0] =='ID') or (o.T[0] =='IF') or (o.T[0] =='WHILE') or (o.T[0] =='READ') or (o.T[0] =='PRINT'):
            Decl_Comando= Syntatic_analyzer('Decl_Comando',[])
            Decl_Comando.filhos.append(self.Comando())
            Decl_Comando.filhos.append(self.Decl_Comando())
            return Decl_Comando
        else:
            return
    def Atribuicao(self):
        print 'Atribuicao'
        #cria um objeto do tipo id
        id_node = self.getNumber(o.T,'ID')
        self.match('ID')
        self.match('ATTR')
        attr_node = Syntatic_analyzer('ATTR',[])
        attr_node.filhos.append(self.ID(id_node))
        attr_node.filhos.append(self.Expressao())
        self.match('PCOMMA')
        return attr_node
    def ID(self,ident,identi='ID'):
        id_node = Syntatic_analyzer(identi,[],0,ident)
        return id_node
    def Bloco(self):
        print 'Bloco'
        self.match('LBRACE')
        bloco = Syntatic_analyzer('Bloco',[])
        bloco.filhos.append(self.Decl_Comando())
        self.match('RBRACE')
        return bloco
    def Declaracoes(self):
        print 'Declaracoes'
        Declaracoes = Syntatic_analyzer('Declaracoes',[])
        Declaracoes.filhos.append(self.Tipo())
        id_node = self.getNumber(o.T,'ID')
        self.match('ID')
        Declaracoes.filhos.append(self.ID(id_node))
        Declaracoes.filhos.append(self.Decl2())
        return Declaracoes
    def Decl2(self):
        print 'Decl2'
        if(o.T[0] == 'COMMA'):
            self.match('COMMA')
            id_node = self.getNumber(o.T,'ID')
            self.match('ID')
            Decl2 =Syntatic_analyzer('Decl2',[])
            Decl2.filhos.append(self.ID(id_node))
            Decl2.filhos.append(self.Decl2())
            return Decl2
        elif(o.T[0] == 'PCOMMA'):
            self.match('PCOMMA')
        elif(o.T[0] == 'ATTR'):
            #criar um nó sintatic analyzer passando um 'ATTR' como argumento
            self.match('ATTR')
            Decl2 =Syntatic_analyzer('Decl2',[])
            Decl2.filhos.append(self.Expressao())
            #attr = Syntatic_analyzer('ATTR')
            #attr.filhos.append(id_node,expr)
            #return attr
            Decl2.filhos.append(self.Decl2())
            return Decl2
    def Tipo(self):
        print 'Tipo'
        if(o.T[0] == 'INT'):
            self.match('INT')
        elif(o.T[0] == 'FLOAT'):
            self.match('FLOAT')
    def Comando(self):
        print 'Comando'
        if(o.T[0] == 'LBRACE'):
            block=Syntatic_analyzer('Comando-Bloco',[])
            block.filhos.append(self.Bloco())
            return block
        elif(o.T[0] == 'IF'):
            comand = Syntatic_analyzer('Comando-Se',[])
            comand.filhos.append(self.ComandoSe())
            return comand
        elif(o.T[0] == 'ATTR' or o.T[0]=='ID' ):
            attr =Syntatic_analyzer('Comando-ATTR',[])
            attr.filhos.append(self.Atribuicao())
            return attr
        elif(o.T[0] == 'WHILE'):
            comand = Syntatic_analyzer('Comando-WHILE',[])
            comand.filhos.append(self.ComandoEnquanto())
            return comand
        elif(o.T[0] == 'READ'):
            return Syntatic_analyzer('Comando-READ',self.ComandoRead())
        elif(o.T[0] == 'PRINT'):
            return Syntatic_analyzer('Comando-PRINT',self.ComandoPrint())
    def ComandoSe(self):
        print 'ComandoSe'
        self.match('IF')
        self.match('LBRACKET')
        comandoSe=Syntatic_analyzer('ComandoSe',[])
        comandoSe.filhos.append(self.Expressao())
        self.match('RBRACKET')
        comandoSe.filhos.append(self.Comando())
        comandoSe.filhos.append(self.ComandoSenao())
        return comandoSe
    def ComandoSenao(self):
        print 'ComandoSenao'
        self.match('ELSE')
        comando= Syntatic_analyzer('ComandoSenao',[])
        comando.filhos.append(self.Comando())
        return comando
    def ComandoEnquanto(self):
        print 'ComandoEnquanto'
        self.match('WHILE')
        self.match('LBRACKET')
        ComandoEnquanto= Syntatic_analyzer('ComandoEnquanto',[])
        ComandoEnquanto.filhos.append(self.Expressao())
        self.match('RBRACKET')
        ComandoEnquanto.filhos.append(self.Comando())
        return ComandoEnquanto
    def ComandoRead(self):
        print 'ComandoRead'
        self.match('READ')
        self.match('ID')
        self.match('PCOMMA')
    def ComandoPrint(self):
        print 'ComandoPrint'
        self.match('PRINT')
        self.match('LBRACKET')
        Cprint = Syntatic_analyzer('ComandoPrint',self.Expressao())
        self.match('RBRACKET')
        self.match('PCOMMA')
        return Cprint
    def Expressao(self):
        print 'Expressao'
        Expressao=    Syntatic_analyzer('Expressao',[])
        Expressao.filhos.append(self.Conjuncao())
        Expressao.filhos.append(self.ExpressaoOpc())
        return Expressao
    def ExpressaoOpc(self):
        print 'ExpressaoOpc'
        if(o.T[0] == 'OR'):
            self.match('OR')
            ExpressaoOpc = Syntatic_analyzer('ExpressaoOpc',[])
            ExpressaoOpc.filhos.append(self.Conjuncao())
            ExpressaoOpc.filhos.append(self.ExpressaoOpc())
            return ExpressaoOpc
    def Conjuncao(self):
        print 'Conjuncao'
        conj =    Syntatic_analyzer('Conjuncao',[])
        conj.filhos.append(self.Igualdade())
        conj.filhos.append(self.ConjuncaoOpc())
        return conj
    def ConjuncaoOpc(self):
        print 'ConjuncaoOpc'
        if(o.T[0] == 'AND'):
            self.match('AND')
            conj= Syntatic_analyzer('ConjuncaoOpc',[])
            conj.filhos.append(self.Igualdade())
            conj.filhos.append(self.ConjuncaoOpc())
            return conj
    def Igualdade(self):
        print 'Igualdade'
        igualdade= Syntatic_analyzer('Igualdade',[])
        igualdade.filhos.append(self.Relacao())
        igualdade.filhos.append(self.IgualdadeOpc())
        return igualdade
    def IgualdadeOpc(self):
        print 'IgualdadeOpc'
        if(o.T[0] == ('EQ' or 'NE')):
            igualdade=  Syntatic_analyzer('IgualdadeOpc',[])
            igualdade.filhos.append(self.OpIgual())
            igualdade.filhos.append(self.Relacao())
            igualdade.filhos.append(self.IgualdadeOpc())
            return igualdade
    def OpIgual(self):
        print 'OpIgual'
        if(o.T[0] == 'EQ'):
            self.match('EQ')
        if(o.T[0] == 'NE'):
            self.match('NE')
    def Relacao(self):
        print 'Relacao'
        relacao= Syntatic_analyzer('Relacao',[])
        relacao.filhos.append(self.Adicao())
        relacao.filhos.append(self.RelacaoOpc())
        return relacao
    def RelacaoOpc(self):
        print 'RelacaoOpc'
        if ( o.T[0] == 'LT' or o.T[0] == 'LE' or o.T[0] == 'GT'or o.T[0] == 'GE'):
            relacao= Syntatic_analyzer('RelacaoOpc',[])
            relacao.filhos.append(self.OpRel())
            relacao.filhos.append(self.Adicao())
            relacao.filhos.append(self.RelacaoOpc())
            return relacao
    def OpRel(self):
        print 'OpRel'
        if(o.T[0] == 'LT'):
            self.match('LT')
        elif(o.T[0] == 'LE'):
            self.match('LE')
        elif(o.T[0] == 'GT'):
            self.match('GT')
        elif(o.T[0] == 'GE'):
            self.match('GE')
    def Adicao(self):
        print 'Adicao'
        add =  Syntatic_analyzer('Adicao',[])
        add.filhos.append(self.Termo())
        add.filhos.append(self.AdicaoOpc())
        return add
    def AdicaoOpc(self):
        print 'AdicaoOpc'
        if(o.T[0] == ('PLUS' or 'MINUS')):
            add =  Syntatic_analyzer('AdicaoOpc',[])
            add.filhos.append(self.OpAdicao())
            add.filhos.append(self.Termo())
            add.filhos.append(self.AdicaoOpc())
            return add
    def OpAdicao(self):
        print 'OpAdicao'
        if(o.T[0] == 'PLUS'):
            self.match('PLUS')
        elif(o.T[0] == 'MINUS'):
            self.match('MINUS')
    def Termo(self):
        print  'Termo'
        term= Syntatic_analyzer('Termo',[])
        term.filhos.append(self.Fator())
        term.filhos.append(self.TermoOpc())
        return term
    def TermoOpc(self):
        print 'TermoOpc'
        if(o.T[0] == ('MULT' or 'DIV')):
            term=  Syntatic_analyzer('TermoOpc',[])
            term.filhos.append(self.OpMult())
            term.filhos.append(self.Fator())
            term.filhos.append(self.TermoOpc())
            return term
    def OpMult(self):
        print 'OpMult'
        if(o.T[0] == 'MULT'):
            mult_node=Syntatic_analyzer('*',[])
            self.match('MULT')
            return mult_node
        elif(o.T[0] == 'DIV'):
            div_node=Syntatic_analyzer('/',[])
            self.match('DIV')
            return div_node
    def Fator(self):
        print 'Fator'
        if(o.T[0] == 'ID'):
            id_node=self.getNumber(o.T,'ID')
            self.match('ID')
            fator=Syntatic_analyzer('Fator',[])
            fator.filhos.append(self.ID(id_node))
            return fator
        if(o.T[0] == 'INTEGER_CONST'):
            id_node=self.getNumber(o.T,'INTEGER_CONST')
            self.match('INTEGER_CONST')
            fator=Syntatic_analyzer('Fator',[])
            fator.filhos.append(self.ID(id_node,'INTEGER_CONST'))
            return fator
        if(o.T[0] == 'FLOAT_CONST'):
            id_node=self.getNumber(o.T,'FLOAT_CONST')
            self.match('FLOAT_CONST')
            fator=Syntatic_analyzer('Fator',[])
            fator.filhos.append(self.ID(id_node,'FLOAT_CONST'))
            return fator
        if(o.T[0] == 'LBRACKET'):
            self.match('LBRACKET')
            ex=Syntatic_analyzer('Expressao',[])
            ex.filhos.append(self.Expressao())
            self.match('RBRACKET')
            fator=Syntatic_analyzer('Fator',[])
            return fator
def printArvore(current_node):
    print "Pai: ",current_node.pai
    if current_node.lexema is not '':
        print 'Lexema: ',current_node.lexema
    for i in current_node.filhos:
        if i is None: None
        else: printArvore(i)


if __name__ == "__main__":
    o=Lexic_analyst()
    o.recognizing()
    filhos=[]
    sintatic = Syntatic_analyzer('AST',[])
    print 'Entrou'
    sintatic.filhos.append(sintatic.Programa())
    print 'Acabou: '
    print sintatic.filhos[0].valor
    printArvore(sintatic)
