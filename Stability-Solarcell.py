import os
import pandas as pd
from datetime import datetime
import re

# Funzione per estrarre la data e ora dal nome del file
def estrai_data(nome_file):
    # Regex per estrarre la data e ora nel formato "YYYY_MM_DD_HH.MM.SS"
    match = re.search(r'(\d{4})_(\d{2})_(\d{2})_(\d{2})\.(\d{2})\.(\d{2})', nome_file)
    if match:
        return datetime(
            int(match.group(1)),  # Anno
            int(match.group(2)),  # Mese
            int(match.group(3)),  # Giorno
            int(match.group(4)),  # Ora
            int(match.group(5)),  # Minuti
            int(match.group(6))   # Secondi
        )
    return None

# Funzione per estrarre il campione e i parametri dal nome del file
def parse_line(line):
    # Rimuove gli spazi tra il campione e "_JV" (se presenti)
    line = line.replace(' _JV', '_JV')  # Rimuove lo spazio prima di "_JV"
    
    date_time = estrai_data(line)
    sample_info = line[24:line.find("_JV")].strip()  # Estrae il nome del campione
    parameters = line[line.find("_JV") + 3:].strip()  # Estrae i parametri dopo "_JV"
    
    return date_time, sample_info, parameters


# dataframe vuoto da riempire dopo
#df = pd.DataFrame(all_data, columns=['DateTime', 'Sample', 'Parameters'])

# Percorso della cartella corrente
current_dir = os.getcwd()

# Lista per memorizzare tutti i dati
all_data = []

# Leggi tutti i file .txt nella cartella corrente
for file_name in os.listdir(current_dir):
    if file_name.endswith(".txt"):
        file_path = os.path.join(current_dir, file_name)
        print(f"Leggendo il file: {file_path}")  # Debug: controlla quale file viene letto
        
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            for line in file:
                # Ignora le righe che sembrano intestazioni o non contengono dati utili
                if line.strip() and not line.startswith("File Name") and not line.startswith('"File'):
                    # Estrai la data e ora, campione e parametri
                    date_time, sample_info, parameters = parse_line(line)
                    #print(date_time , " " , sample_info , " " , parameters)
                    substrate_name = re.search(r'_S\d{1,2}', sample_info).group()[1:]
                    print(sample_info)
                    cell_number = sample_info[1]
                    cell_complete = substrate_name + cell_number
                    all_data.append([date_time, cell_complete, sample_info, parameters])  # Salva i dati

df = pd.DataFrame(all_data, columns=['DateTime', 'Cell', 'sample_info', 'Parameters'])

 # Ordina i dati cronologicamente per campione
df_sorted = df.sort_values(by=['Cell', 'DateTime'])

#TODO df_sorted non ha tutti i dati
 # Gruppo i dati per campione
grouped = df_sorted.groupby('Cell')

for sample, group in grouped:
	os.makedirs('./dmp', exist_ok=True)
	output_file_name = f"dmp/{sample}_output.txt"
	output_file_path = os.path.join(current_dir, output_file_name)
			
			# Scrive i dati per il campione
	with open(output_file_path, 'w') as output_file:
		output_file.write("DateTime;Cell;sample_info;Parameters\n")
		for index, row in group.iterrows():
			output_file.write(f"{row['DateTime']};{row['Cell']};{row['sample_info']};{row['Parameters']}\n")

	print(f"File salvato: {output_file_path}")

print(df)
print(df_sorted)
