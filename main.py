import sched
import time
from threading import Thread
import webbrowser
import os

os.environ['MENS'] = ''

# classe que armazena os links a serem abertos
class Evento():

    HORA = 0
    MIN = 1

    def __init__(self, link, hora):#paremetro hora é uma string que representa hora '16:30'
        self.link = link
        self.hora = hora
        self.momento_time = self.str_2_momento(hora) #Objeto do tipo time responsavél por armazenar hora do evento
        self.hora_minuto = self.split_hora_minuto(hora)

    # função recebe string do tipo '20:09'
    # função devolve tupla contendo hora e minuto
    def split_hora_minuto(self, horas):
        hora_min = horas.split(':')
        horario = int(hora_min[0]), int(hora_min[1])
        return horario

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
        super().__init__()
        self.rodando = True
        self.evento = evento
        timer_segundo_atual = int(time.time())
        timer_segundo_evento = int(self.evento.momento_time)
        timer_segundos_diferenca =  timer_segundo_evento - timer_segundo_atual
        self.tarefa_concluida = False

        if timer_segundos_diferenca < 0:
            raise ValueError('Evento com tempo já passado')

    def run(self) -> None:

        # Levanta exeção caso o valor da diferenca do tempo do evento e
        # o tempo atual seja menor que 0


        while self.rodando:
            tmp_atual = time.gmtime()
            if tmp_atual.tm_hour - 3 == self.evento.hora_minuto[Evento.HORA]:
                if tmp_atual.tm_min == self.evento.hora_minuto[Evento.MIN]:
                    break
            time.sleep(.5)
        if self.rodando:
            webbrowser.open_new_tab(self.evento.link)
        self.tarefa_concluida = True
        return super().run()

class Links_exibicao():

    def __init__(self, app):
        self.tarefas = []# Todas tarefas adicionadas, armazenada em objetos Tarefas
        self.mensagens = ''
        self.app = app

    def get_status(self):
        for t in self.tarefas:
            self.mensagens += t.evento.link + ' - ' + t.evento.hora + '  executando\n'
        if self.mensagens == '':
            self.mensagens = 'Todos os horários já passaram.'
        return self.mensagens

    def adiciona_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def get_mensagens(self):
        return self.mensagens

    def iniciar(self):
        arq_links = open('links.conf')
        
        for line in arq_links:
            if line[0] == '#' or line[0] == ' ' or line[0] == '\t' or line[0] == '\n':
                continue
            dados_evento = line.strip().split(' ')
            link = dados_evento[0]
            instante = dados_evento[-1]

            evento = Evento(link=link, hora=instante)
            try:
                tarefa = Tarefas(evento=evento)
                self.adiciona_tarefa(tarefa=tarefa)
            except:
                os.environ['MENS'] += link + ' - ' + instante + ' -> Hora já passou.\n'
                continue

        for tarefa in self.tarefas:
            tarefa.start()