import sched
import time
from threading import Thread

class Evento():
    def __init__(self, link, hora):#paremetro hora é uma string que representa hora '16:30'
        self.link = link
        self.momento_segundos = self.str_2_momento(hora) #Objeto do tipo time responsavél por armazenar hora do evento

    #Retorna segundos do evento desde a era
    #usa como dia padrão o dia atual
    def str_2_momento(self, hora):
        hora_min = hora.split(':')
        hora = int(hora_min[0])
        minuto = int(hora_min[1])

        # cria novo segundos desde a era de acordo com a data atual
        data_hora_atual = time.gmtime()
        momento = time.mktime((
            data_hora_atual.tm_year,
            data_hora_atual.tm_mon,
            data_hora_atual.tm_mday,
            hora,
            minuto,
            data_hora_atual.tm_sec,
            data_hora_atual.tm_wday,
            data_hora_atual.tm_yday,
            data_hora_atual.tm_isdst
        ))
        
        return momento

class Tarefas(Thread):
    def __init__(self, evento):
        self.evento = evento

    def run(self) -> None:

        return super().run()


class Links_exibicao():
    def __init__(self):
        # variavél que armazena os links a serem abertos
        # cada espaço de vetor conterá um objeto Evento
        # que armazena dados para o evento que ocorrerá
        # de forma determinada no arquivo .conf
        self.eventos = []
        self.tarefas = []# Todas tarefas adicionadas, armazenada em objetos Tarefas 

    def adiciona_Evento(self, evento):
        self.eventos.append(evento)
