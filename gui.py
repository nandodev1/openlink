import time
import main
from threading import Thread
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit
import os



class Open_link(Thread):

    def __init__(self) -> None:
        self.area_texto = None
        self.link_exibicao = None
        self.mensagens = ''

    def iniciar(self):

        app = QApplication(sys.argv)
        w = QWidget()
        w.resize(600,300)
        w.setWindowTitle('OPEN LINK')
        label = QLabel(w)
        label.setText("<=== OPEN LINK ===>")
        label.move(22,10)
        label.show()

        self.area_texto = QTextEdit(w)
        self.area_texto.move(22, 30)
        self.area_texto.setReadOnly(True)
        self.area_texto.resize(556,220)
        self.area_texto.show()

        btn1 = QPushButton(w)
        btn1.setText('INICIAR')
        btn1.move(22,260)

        btn2 = QPushButton(w)
        btn2.setText('PARAR')
        btn2.move(500,260)

        btn3 = QPushButton(w)
        btn3.setText('LINPAR LOG')
        btn3.move(260,260)

        btn1.show()
        btn1.clicked.connect(self.run)

        btn2.show()
        btn2.clicked.connect(self.parar)

        btn3.show()
        btn3.clicked.connect(self.linpar)

        
        w.show()
        sys.exit(app.exec_())
        breakpoint

    def adiciona_mensagem(self, mensagem):
        os.environ['MENS'] += mensagem + '\n'
        self.area_texto.setText(os.environ['MENS'])

    def run(self):
        if self.link_exibicao == None:
            self.link_exibicao = main.Links_exibicao()
            self.adiciona_mensagem('Programa iniciado.')
            self.link_exibicao.iniciar()
            mensagens = self.link_exibicao.get_status()
            self.adiciona_mensagem(mensagens)
        else:
            self.adiciona_mensagem('Seu programa já esta iniciado.')
            
    def parar(self):
        self.linpar()
        if self.link_exibicao != None:
            self.link_exibicao = None
            self.adiciona_mensagem('Programa parado.')
        else:
            self.adiciona_mensagem('Seu programa já esta parado.')

    def linpar(self):
            os.environ['MENS'] = ''
            self.area_texto.setText(self.mensagens)

    def atualiza_mensagem(self):
            if self.link_exibicao != None:
                self.mensagens += self.link_exibicao.get_mensagens
                self.area_texto.setText(self.mensagens)

oplink = Open_link()
oplink.iniciar()