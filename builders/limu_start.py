from core.builder import *

start_script = """#!/bin/sh
echo "Welcome to limu."
set -x
umask 022
export LC_ALL=POSIX
export PATH=$PATH:/usr/bin
export PATH
mkdir -p /run /var/run
dhcpcd
Xorg &
sleep 1
export DISPLAY=:0.0
fluxbox &
sleep 1
xterm &
dillo &
echo "Starting bash, X should start shortly."
sleep 1
bash
"""

as_root = """#!/bin/sh
su -
"""

def Versions():
    return ['0.1']

def Build():
    Mkdir(Dest())
    Chdir(Dest())
    File('user.sh', start_script)
    Execute('chmod +x user.sh')
    File('as_root.sh', as_root)
    Execute('chmod +x as_root.sh')
    Execute('chmod +s as_root.sh')
