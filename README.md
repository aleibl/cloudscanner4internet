ENGLISH VERSION BELOW

# cloudscanner4internet
Un conjunto de scripts para realizar un escaneo de todo Internet o parte de él utilizando posiblemente cientos de máquinas virtuales en la nube

## Configuración
Tendrás que crear tus propias Imágenes de Máquina de Amazon (AMIs) y distribuirlas a las regiones que quieras utilizar, después añade los AMI-IDs al script.

### Crear tu imagen de máquina virtual
Imagen inicial recomendada: Rocky Linux (pero debería funcionar con la mayoría de distribuciones Linux recientes).

Inicia tu máquina Rocky Linux y ejecuta los siguientes pasos como root:

```
dnf install nmap
dnf install tmux
dnf install vim-enhanced
dnf install wget
dnf install git make gcc
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
ln -s /usr/lib64/libpcap.so.1 /usr/lib64/libpcap.so
```

Crea tu AMI a partir de esta máquina, distribúyela a las regiones que quieras utilizar y añade sus IDs al script aws-run-scan.py.

# cloudscanner4internet
A set of scripts to perform a scan of the entire internet or portion thereof using possibly hundreds of cloud VMs

## Setup
You will need to create your own Amazon Machine Images (AMIs) and distribute them to the regions you want to use, then add the AMI-IDs to the script.

### Creating your virtual machine image
Recommended starting image: Rocky Linux (but it should work with most recent Linux distributions).

Start your Rocky Linux machine and execute the following steps as root:

```
dnf install nmap
dnf install tmux
dnf install vim-enhanced
dnf install wget
dnf install git make gcc
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
ln -s /usr/lib64/libpcap.so.1 /usr/lib64/libpcap.so
```

Create your AMI from this machine, distribute it to the regions you want to use and add their IDs to the aws-run-scan.py script.

