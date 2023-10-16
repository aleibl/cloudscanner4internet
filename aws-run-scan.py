#!/usr/bin/python3

import os
import datetime
import time

# tienes que rellenar aquí tus propios identificadores AMI
regions = { "us-east-1":      {"name": "N. Virginia", "ami-id": "ami-xxxxxxxxxxxxxxxxx"},
            "us-west-2":      {"name": "Oregon",      "ami-id": "ami-xxxxxxxxxxxxxxxxx"},
            "ap-south-1":     {"name": "Mumbai",      "ami-id": "ami-xxxxxxxxxxxxxxxxx"},
            "ap-south-2":     {"name": "Hyderabad",   "ami-id": "ami-xxxxxxxxxxxxxxxxx"},
            "ap-southeast-1": {"name": "Singapore",   "ami-id": "ami-xxxxxxxxxxxxxxxxx"}
          }

# Ejemplos de configuración:
# AFRINIC  7 redes /8 -> 2  nodos trabajadores
# LACNIC  10 redes /8 -> 3  nodos trabajadores
# RIPE    44 redes /8 -> 11 nodos trabajadores
# APNIC   51 redes /8 -> 13 nodos trabajadores
# ARIN    92 redes /8 -> 23 nodos trabajadores
# Total: 52 workers (64 max en 4 regions, max 16 cada region @ 2vCPUs/worker)
#workers = [
#            { "AFRINIC": {"ap-south-2": 2} },
#            { "LACNIC": {"us-west-2": 3} },
#            { "RIPE": {"us-east-1": 6, "ap-south-1": 5} },
#            { "APNIC": {"ap-south-1": 7, "ap-south-2": 6} },
#            { "ARIN": {"us-west-2": 13, "us-east-1": 10} }
#          ]

# AFRINIC  7 redes /8 -> 5  nodos trabajadores
# LACNIC  10 redes /8 -> 7  nodos trabajadores
# RIPE    44 redes /8 -> 27 nodos trabajadores
# APNIC   51 redes /8 -> 32 nodos trabajadores
# ARIN    92 redes /8 -> 57 nodos trabajadores
# Total: 128 workers (128 max en 4 regions, max 32 cada region @ 1 vCPU/worker)
#workers = [
#            { "AFRINIC": {"ap-southeast-1": 5} },
#            { "LACNIC": {"us-west-2": 7} },
#            { "RIPE": {"ap-south-1": 17, "ap-southeast-1": 10} },
#            { "APNIC": {"ap-south-1": 15, "ap-southeast-1": 17} },
#            { "ARIN": {"us-west-2": 25, "us-east-1": 32} }
#          ]

# AFRINIC  7 redes /8 -> 6  nodos trabajadores
# LACNIC  10 redes /8 -> 8  nodos trabajadores
# RIPE    44 redes /8 -> 34 nodos trabajadores
# APNIC   51 redes /8 -> 40 nodos trabajadores
# ARIN    92 redes /8 -> 72 nodos trabajadores
# Total 72+40+34+8+6=160 (160 max en 5 regions, max 32 cada region @ 1 vCPU/worker)
workers = [
            { "AFRINIC": {"us-west-2": 1, "us-east-1": 1, "ap-south-1": 2, "ap-southeast-1": 1, "ap-south-2": 1} },
            { "LACNIC":  {"us-west-2": 1, "us-east-1": 1, "ap-south-1": 2, "ap-southeast-1": 2, "ap-south-2": 2} },
            { "RIPE":    {"us-west-2": 7, "us-east-1": 7, "ap-south-1": 7, "ap-southeast-1": 7, "ap-south-2": 6} },
            { "APNIC":   {"us-west-2": 8, "us-east-1": 8, "ap-south-1": 8, "ap-southeast-1": 8, "ap-south-2": 8} },
            { "ARIN":    {"us-west-2": 15, "us-east-1": 15, "ap-south-1": 13, "ap-southeast-1": 14, "ap-south-2": 15} }
          ]

# variables generales
log = []
job_id = "TFM-fullscan03-p80-160w-01"   # nombre del trabajo - se utilizará en los nombres de archivos y carpetas
#instance_type = "m6g.large"
instance_type = "m6g.medium"
#instance_type = "m7g.medium"   # no disponible en ap-south-2
key_name = "NOMBRE-CLASE"    # aquí se requiere un nombre válido de clave
security_groups = "NOMBRE-SECURITY-GROUP"   #aquí se requiere un nombre válido de grupo de seguridad
port = 80        
mode = "full"   # "full" o "test"
scan_method = "masscan"   # "masscan" o "nmap"
grab_banner = "no"   # "yes" o "no"
wait_secs = 5
rate_per_sec = 600000
shutdown = "yes"   # "yes" o "no"
aws_shutdown_behavior = "terminate"
start_timestamp = 0

print("¡Bienvenido al escáner paralelo masivo en la nube para Internet!")

# registrar hora de inicio
start_time = datetime.datetime.now()
print(f"Start time: {start_time} UTC")
timer_at_start = time.perf_counter()

for region in regions.keys():
  print(region)
  print(regions[region]['name'])
  print(regions[region]['ami-id'])

# calcular el número de trabajadores por rir (registro regional de internet)
total_workers = 0
total_workers_rir = {}
for worker_dict in workers:
  rir = list(worker_dict.keys())[0]
  print(rir)
  rir_awsregions = list(worker_dict[rir].keys())
  total_workers_rir[rir] = 0
  for rir_awsregion in rir_awsregions:
    workers_no = worker_dict[rir][rir_awsregion]
    total_workers += workers_no
    total_workers_rir[rir] += workers_no
    print(f"  {rir_awsregion}: {workers_no}")
    log.append(f"  {rir_awsregion}: {workers_no}")
  print(f"  Total: {total_workers_rir[rir]}")
  log.append(f"  Total: {total_workers_rir[rir]}")
print(f"Total: {total_workers}")
log.append(f"Total: {total_workers}")

print(regions)
# generar y ejecutar comandos aws cli run-instances
for worker_dict in workers:
  rir = list(worker_dict.keys())[0]
  print(rir)
  rir_awsregions = list(worker_dict[rir].keys())
  instance_no = 0
  for rir_awsregion in rir_awsregions:
    workers_no = worker_dict[rir][rir_awsregion]
    for dummy in range (1, workers_no + 1):
      instance_no += 1
      print(f"  {rir_awsregion}: {instance_no} of {total_workers_rir[rir]}")
      cmd = f"aws ec2 --region {rir_awsregion} run-instances --image-id {regions[rir_awsregion]['ami-id']} --count 1 --instance-type {instance_type} "
      cmd += f"--key-name {key_name} --security-groups {security_groups} "
      cmd += f"--tag-specifications ResourceType=instance,Tags=[{{Key=job_id,Value={job_id}}},{{Key=rir,Value={rir}}},"
      cmd += f"{{Key=instances_in_rir,Value={total_workers_rir[rir]}}},{{Key=scan_instance,Value={instance_no}}},{{Key=mode,Value={mode}}},{{Key=scan_method,Value={scan_method}}},"
      cmd += f"{{Key=grab_banner,Value={grab_banner}}},{{Key=wait_secs,Value={wait_secs}}},{{Key=port,Value={port}}},{{Key=rate_per_sec,Value={rate_per_sec}}},"
      cmd += f"{{Key=shutdown,Value={shutdown}}},{{Key=start_timestamp,Value={start_timestamp}}}] "
      cmd += f"--metadata-options HttpTokens=required,HttpPutResponseHopLimit=1,HttpEndpoint=enabled,HttpProtocolIpv6=disabled,InstanceMetadataTags=enabled "
      cmd += f"--instance-initiated-shutdown-behavior {aws_shutdown_behavior} --no-cli-pager --no-cli-auto-prompt --output text"
      print(cmd)
      log.append(cmd)
      output = os.popen(cmd).read()
      print(output)
      log.append(output)

# registrar hora final
timer_at_finish = time.perf_counter()
end_time = datetime.datetime.now()
print(f"End time: {end_time} UTC")

# tiempo de ejecución de este script (inicio de instancias AWS)
execution_time =f"{timer_at_finish - timer_at_start:0.4f}"
print(f"Execution time of this script: {execution_time} seconds")

info_file = f"{job_id}-aws.info.txt"
with open(info_file, "w") as info:
  info.write(f"Job: {job_id}\n")
  info.write(f"Start time: {start_time} UTC\n")
  info.write(f"End time: {end_time} UTC\n")
  info.write(f"Execution time of this script: {execution_time} seconds\n\n")
  info.write("\n".join(log))
info.close()

# sustituye "NOMBRE-DE-S3-BUCKET" por el nombre de tu bucket S3 en el que quieres escribir los datos
copy_cmd = f"aws s3 cp {info_file} s3://NOMBRE-DE-S3-BUCKET/"
print(copy_cmd)
os.system(copy_cmd)

