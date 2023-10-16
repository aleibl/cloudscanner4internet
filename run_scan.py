#!/usr/bin/python3

import requests
import os
import time
import datetime
import uuid
import subprocess
import math

# Paso 1: Obtener parámetros
params = {}

headers = {
    'X-aws-ec2-metadata-token-ttl-seconds': '21600',
}

token = requests.put('http://169.254.169.254/latest/api/token', headers=headers).text

headers = {
    'X-aws-ec2-metadata-token': token
}

response = requests.get('http://169.254.169.254/latest/meta-data/tags/instance/', headers=headers).text
for key in response.splitlines():
  value = requests.get('http://169.254.169.254/latest/meta-data/tags/instance/' + key, headers=headers).text
  params[key] = value

print(params)
# Ejemplo: {'instances_in_rir': '1', 'mode': 'test', 'rir': 'ARIN', 'scan_instance': '1', 'scan_method': 'masscan', 'shutdown': 'yes'}

# Paso 2: Configurar el escaneo
if params.get('mode') == None:
  print("Parameter 'mode' not present, aborting...")
  exit(1)
if params['mode'] == "test":
  print("Test mode, only scanning a few IP block...")
elif params['mode'] == "full":
  print("Full scan mode, scanning all my IP blocks...")
else:
  print("Unknown scan mode '" + params['mode'] + "', aborting...")
  exit(1)

if params.get('instances_in_rir') == None:
  print("Parameter 'instances_in_rir' not present, aborting...")
  exit(1)
params['instances_in_rir'] = int(params['instances_in_rir'])
if params['instances_in_rir'] > 0:
  print("Running " + str(params['instances_in_rir']) + " instances...")
else:
  print("Illegal number of instances '" + str(params['instances_in_rir']) + "', aborting...")
  exit(1)

if params.get('scan_instance') == None:
  print("Parameter 'scan_instance' not present, aborting...")
  exit(1)
params['scan_instance'] = int(params['scan_instance'])
if params['scan_instance'] > 0 and params['scan_instance'] <= params['instances_in_rir']:
  print("Running as number " + str(params['scan_instance']) + " of " + str(params['instances_in_rir']) + " instances...")
else:
  print("Illegal instance number '" + str(params['scan_instance']) + "', aborting...")
  exit(1)

# rir
if params.get('rir') == None:
  print("Parameter 'rir' not present, aborting...")
  exit(1)
if params['rir'] == "AFRINIC":
  print("RIR = " + params['rir'])
elif params['rir'] == "APNIC":
  print("RIR = " + params['rir'])
elif params['rir'] == "ARIN":
  print("RIR = " + params['rir'])
elif params['rir'] == "LACNIC":
  print("RIR = " + params['rir'])
elif params['rir'] == "RIPE":
  print("RIR = " + params['rir'])
else:
  print("Unknown RIR '" + params['rir'] + "', aborting...")
  exit(1)

# número del puerto
if params.get('port') == None:
  print("Parameter 'port' not present, aborting...")
  exit(1)
params['port'] = int(params['port'])
if params['port'] >= 0 and params['port'] <= 65535:
  print("Port number " + str(params['port']))
else:
  print("Illegal port number '" + str(params['port']) + "', aborting...")
  exit(1)

# banner grabbing si o no?
if params.get('grab_banner') == None:
  print("Parameter 'grab_banner' not present, aborting...")
  exit(1)
if params['grab_banner'] == "yes":
  print("Grabbing banners (slower) (NOT YET IMPLEMENTED)...")
elif params['grab_banner'] == "no":
  print("Not grabbing banners (faster)...")
else:
  print("Unknown grab_banner value '" + params['grab_banner'] + "', aborting...")
  exit(1)

# job_id (transmitido o generado)
if params.get('job_id') == None:
  params['job_id'] = str(uuid.uuid4())
  print("Parameter 'job_id' not passed, generated '" + params['job_id'] + "'")
else:
  print("job_id = '" + params['job_id'] + "'")

# tasa por segundo (sólo relevante para masscan)
if params.get('rate_per_sec') == None:
  params['rate_per_sec'] = 500000
  print("Parameter 'rate_per_sec' not passed, defaulting to '" + str(params['rate_per_sec']) + "'")
else:
  params['rate_per_sec'] = int(params['rate_per_sec'])
  print("rate_per_sec = '" + str(params['rate_per_sec']) + "'")

# tiempo de espera en segundos (only relevant for masscan)
if params.get('wait_secs') == None:
  params['wait_secs'] = 10
  print("Parameter 'wait_secs' not passed, defaulting to '" + (params['wait_secs']) + "'")
else:
  params['wait_secs'] = int(params['wait_secs'])
  print("wait_secs = '" + str(params['wait_secs']) + "'")

# start_timestamp (marca de tiempo Unix en UTC, falta o 0 significa "ahora")
if params.get('start_timestamp') == None:
  params['start_timestamp'] = datetime.datetime.utcnow().timestamp()
  print("Parameter 'start_timestamp' not passed, defaulting to 'now'" + (params['start_timestamp']) + "'")
else:
  params['start_timestamp'] = int(params['start_timestamp'])
  if params['start_timestamp'] <= 0:
    params['start_timestamp'] = math.floor(datetime.datetime.utcnow().timestamp())
    print("Parameter 'start_timestamp' is zero, defaulting to 'now'" + str(params['start_timestamp']) + "'")
  else:
    params['start_timestamp'] = int(params['start_timestamp'])
    print("start_timestamp = '" + str(params['start_timestamp']) + "'")
    now_timestamp = math.floor(datetime.datetime.utcnow().timestamp())
    print("now_timestamp = '" + str(now_timestamp) + "'")
    wait_secs = params['start_timestamp'] - now_timestamp
    while wait_secs > 0:
      print("sleeping for = " + str(wait_secs) + " seconds")
      time.sleep(wait_secs)
      now_timestamp = math.floor(datetime.datetime.utcnow().timestamp())
      print("now_timestamp = '" + str(now_timestamp) + "'")
      wait_secs = params['start_timestamp'] - now_timestamp

# Paso 3: ejecutar el escaneo
if params.get('scan_method') == None:
  print("Parameter 'scan_method' not present, aborting...")
  exit(1)

# record start time
start_time = datetime.datetime.utcnow()
print(f"Start time: {start_time} UTC")
print(f"Start time: {start_time.timestamp()}")
timer_at_start = time.perf_counter()
line_no = 0
input_path = "/root"
#output_path = "/root/output"
output_root = f"/root/output"
output_path = f"{output_root}/{params['job_id']}"
try:
  os.mkdir(output_path)
except Exception as e:
  print(e)

if params['scan_method'] == "masscan":
  print("Scanning with masscan...")
  with open(f"{input_path}/{params['rir']}-ip2asn-v4-4c.tsv", "r") as input_file, open(f"{input_path}/masscan-range", "w") as range_file:
    for line in input_file:
      if line.startswith("#"):
        continue
      else:
        line_no += 1
        if (line_no % params['instances_in_rir']) + 1 != params['scan_instance']:
          continue
        cols = line.rstrip().split("\t")
        class_a_block = cols[0]
        rir     = cols[1]
        ipstart = cols[2]
        ipend   = cols[3]
        ipcount = cols[4]
        range_file.write(f"{ipstart}-{ipend}\n")
        if params['mode'] == "test" and line_no > 10*params['instances_in_rir']:
          break

  range_file.close()
  output_file = f"{output_path}/{params['job_id']}-{params['rir']}-{params['scan_instance']}-of-{params['instances_in_rir']}.txt"
  print(output_file)
  command_array = ["/root/masscan/bin/masscan", "--rate", f"{params['rate_per_sec']}", "--wait", f"{params['wait_secs']}", "-p", f"{params['port']}", "-iL", f"{input_path}/masscan-range", "-oL", f"{output_file}"]
  scan_process_result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  print(scan_process_result.stdout.decode('utf-8'))
  print(scan_process_result.stderr.decode('utf-8'))

elif params['scan_method'] == "nmap":
  print("Scanning with nmap...")
  with open(f"{input_path}/{params['rir']}-ip2asn-v4-4c.tsv", "r") as input_file, open(f"{input_path}/nmap-range", "w") as range_file:
    for line in input_file:
      if line.startswith("#"):
        continue
      else:
        line_no += 1
        if (line_no % params['instances_in_rir']) + 1 != params['scan_instance']:
            continue;
        cols = line.rstrip().split("\t")
        class_a_block = cols[0]
        rir     = cols[1]
        ipstart = cols[2]
        ipend   = cols[3]
        ipcount = cols[4]
        range_file.write(f"{ipstart}-{ipend}\n")
        if params['mode'] == "test":
          break

  range_file.close()
  ipstart = "134.60.66.0"
  blocksize = "24"
  ipblock = f"{ipstart}/{blocksize}"
  output_file = f"{output_path}/{params['job_id']}-{ipstart}-{blocksize}.txt"
  command = f"nmap -n -sS -oA {output_file} -p {params['port']} {ipstart}/{blocksize}"
  print(command)
  os.system(command)
else:
  print("Unknown scan method '" + params['scan_method'] + "', aborting...")
  exit(1)

# registrar hora de finalización
timer_at_finish = time.perf_counter()
end_time = datetime.datetime.utcnow()
print(f"End time: {end_time} UTC")
print(f"End time: {end_time.timestamp()}")

# tiempo de ejecución del escaneo
scan_time =f"{timer_at_finish - timer_at_start:0.4f}"
print(f"Execution time of the scan: {scan_time} seconds")
info_file = f"{output_path}/{params['job_id']}-{params['rir']}-{params['scan_instance']}-of-{params['instances_in_rir']}.info.txt"
with open(info_file, "w") as info:
  info.write(f"Scan method: {params['scan_method']}\n")
  info.write(f"Wait time: {params['wait_secs']} s\n")
  info.write(f"Mode: {params['mode']}\n")
  info.write(f"Port: {params['port']}\n")
  info.write(f"RIR: {params['rir']}\n")
  info.write(f"Running as number {str(params['scan_instance'])} of {str(params['instances_in_rir'])} instances\n")
  info.write(f"Start time: {start_time} UTC\n")
  info.write(f"Start time: {start_time.timestamp()}\n")
  info.write(f"End time: {end_time} UTC\n")
  info.write(f"End time: {end_time.timestamp()}\n")
  info.write(f"Execution time of the scan: {scan_time} seconds\n")
  info.write(scan_process_result.stdout.decode('utf-8'))
  info.write(scan_process_result.stderr.decode('utf-8'))
info.close()

# Paso 4: Copiar los resultados
job_id = params['job_id']
# sustituye "NOMBRE-DE-S3-BUCKET" por el nombre de tu bucket S3 en el que quieres escribir los datos
copy_cmd = f"/usr/local/bin/aws s3 sync {output_root} s3://NOMBRE-DE-S3-BUCKET/ --exclude '*' --include '{job_id}/*'"
print(copy_cmd)
os.system(copy_cmd)

# Paso 5: Apagar si se solicita
if params['shutdown'] == "yes":
  print("Scan complete, shutting down...")
  os.system("/sbin/shutdown -h now")   # esto se apagará inmediatamente
  # os.system("/sbin/shutdown")        # esto esperará 60 segundos antes de apagarse 
else:
  print("Scan complete, but no shutdown requested...")


