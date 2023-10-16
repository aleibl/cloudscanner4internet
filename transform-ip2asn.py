#!/usr/bin/python3

import ipaddress

ip_blocks_2_include = {}
file_ip_blocks_2_include = "ip-blocks-2-include.tsv"
with open(file_ip_blocks_2_include) as file:
  for line in file:
    if line.startswith("#"):
      continue
    else:
      # include/exclude block rir/organization
      cols = line.rstrip().split("\t")
      if cols[0] == "exclude":
        continue
      if cols[0] == "include":
        ip_blocks_2_include[cols[1]] = cols[2]
      else:
        print("ERROR: " + line.rstrip())

file_ip2asn = "ip2asn-v4.tsv"
count_nets_included = 0
count_nets_not_included = 0
count_nets_not_routed = 0
count_ips_included = 0
stats_blocksize = {}
ip_count_rir = {"AFRINIC": 0, "APNIC": 0, "ARIN": 0, "LACNIC": 0, "RIPE": 0, "AFRINIC4c": 0, "APNIC4c": 0, "ARIN4c": 0, "LACNIC4c": 0, "RIPE4c": 0}

with open(file_ip2asn, "r") as input_file, open("AFRINIC-ip2asn-v4.tsv", "w") as afrinic, open("AFRINIC-ip2asn-v4-4c.tsv", "w") as afrinic4c, open("APNIC-ip2asn-v4.tsv", "w") as apnic, open("APNIC-ip2asn-v4-4c.tsv", "w") as apnic4c, open("ARIN-ip2asn-v4.tsv", "w") as arin, open("ARIN-ip2asn-v4-4c.tsv", "w") as arin4c, open("LACNIC-ip2asn-v4.tsv", "w") as lacnic, open("LACNIC-ip2asn-v4-4c.tsv", "w") as lacnic4c, open("RIPE-ip2asn-v4.tsv", "w") as ripe, open("RIPE-ip2asn-v4-4c.tsv", "w") as ripe4c:
  for line in input_file:
    if line.startswith("#"):
      continue
    else:
      cols = line.rstrip().split("\t")
      # range_start range_end AS_number country_code AS_description
      # 1.0.0.0 1.0.0.255       13335   US      CLOUDFLARENET
      # ['1.0.0.0', '1.0.0.255', '13335', 'US', 'CLOUDFLARENET']
      ip_start = cols[0]
      ip_end   = cols[1]
      country_code = cols[3]
      as_desc = cols[4]

      ip_count = int(ipaddress.IPv4Address(ip_end)) - int(ipaddress.IPv4Address(ip_start)) + 1
      class_a_block = ip_start.split('.')[0] + '.0.0.0/8'

      if ip_blocks_2_include.get(class_a_block) == None:
        count_nets_not_included += 1
        continue

      rir = ip_blocks_2_include[class_a_block]
      if rir == "RIPE NCC":
        rir = "RIPE"
      as_number = int(cols[2])

      # 1.0.1.0 1.0.3.255       0       None    Not routed
      if as_number < 1:
        count_nets_not_routed += 1
        continue

      if stats_blocksize.get(ip_count) == None:
        stats_blocksize[ip_count] = 1
      else:
        stats_blocksize[ip_count] += 1

      count_nets_included += 1
      count_ips_included  += ip_count
      output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
      ip_count_rir[rir] += ip_count

      if rir == "RIPE":
        ripe.write(output)
        while ip_count > 1024:
          ip_end_tmp = ipaddress.IPv4Address(ip_start) + 1024 - 1
          ip_count_tmp = int(ipaddress.IPv4Address(ip_end_tmp)) - int(ipaddress.IPv4Address(ip_start)) + 1
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end_tmp}\t{ip_count_tmp}\n"
          ripe4c.write(output)
          ip_start = ip_end_tmp + 1
          ip_count -= 1024
          ip_count_rir[f"{rir}4c"] += 1024
        if ip_count > 0:
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
          ripe4c.write(output)
          ip_count_rir[f"{rir}4c"] += ip_count

      elif rir == "AFRINIC":
        afrinic.write(output)
        while ip_count > 1024:
          ip_end_tmp = ipaddress.IPv4Address(ip_start) + 1024 - 1
          ip_count_tmp = int(ipaddress.IPv4Address(ip_end_tmp)) - int(ipaddress.IPv4Address(ip_start)) + 1
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end_tmp}\t{ip_count_tmp}\n"
          afrinic4c.write(output)
          ip_start = ip_end_tmp + 1
          ip_count -= 1024
          ip_count_rir[f"{rir}4c"] += 1024
        if ip_count > 0:
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
          afrinic4c.write(output)
          ip_count_rir[f"{rir}4c"] += ip_count

      elif rir == "APNIC":
        apnic.write(output)
        while ip_count > 1024:
          ip_end_tmp = ipaddress.IPv4Address(ip_start) + 1024 - 1
          ip_count_tmp = int(ipaddress.IPv4Address(ip_end_tmp)) - int(ipaddress.IPv4Address(ip_start)) + 1
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end_tmp}\t{ip_count_tmp}\n"
          apnic4c.write(output)
          ip_start = ip_end_tmp + 1
          ip_count -= 1024
          ip_count_rir[f"{rir}4c"] += 1024
        if ip_count > 0:
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
          apnic4c.write(output)
          ip_count_rir[f"{rir}4c"] += ip_count

      elif rir == "ARIN":
        arin.write(output)
        while ip_count > 1024:
          ip_end_tmp = ipaddress.IPv4Address(ip_start) + 1024 - 1
          ip_count_tmp = int(ipaddress.IPv4Address(ip_end_tmp)) - int(ipaddress.IPv4Address(ip_start)) + 1
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end_tmp}\t{ip_count_tmp}\n"
          arin4c.write(output)
          ip_start = ip_end_tmp + 1
          ip_count -= 1024
          ip_count_rir[f"{rir}4c"] += 1024
        if ip_count > 0:
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
          arin4c.write(output)
          ip_count_rir[f"{rir}4c"] += ip_count


      elif rir == "LACNIC":
        lacnic.write(output)
        while ip_count > 1024:
          ip_end_tmp = ipaddress.IPv4Address(ip_start) + 1024 - 1
          ip_count_tmp = int(ipaddress.IPv4Address(ip_end_tmp)) - int(ipaddress.IPv4Address(ip_start)) + 1
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end_tmp}\t{ip_count_tmp}\n"
          lacnic4c.write(output)
          ip_start = ip_end_tmp + 1
          ip_count -= 1024
          ip_count_rir[f"{rir}4c"] += 1024
        if ip_count > 0:
          output = f"{class_a_block}\t{rir}\t{ip_start}\t{ip_end}\t{ip_count}\n"
          lacnic4c.write(output)
          ip_count_rir[f"{rir}4c"] += ip_count

      else:
        print(f"Unknown RIR '{rir}', aborting...")
        exit(1)

print(f"Summary: count_nets_included={count_nets_included}, count_nets_not_included={count_nets_not_included}, count_nets_not_routed={count_nets_not_routed}, count_ips_included={count_ips_included}")
print(ip_count_rir)






