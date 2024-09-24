import os

os.chdir('/home/isaque/PycharmProjects/gameficacao_secit_server/api/managers')
filenames = os.listdir('../models')

for filename in filenames:
    os.system(f"touch {filename}")
