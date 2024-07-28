Introduction
------------

Limu is a prototype for a deterministic from-source Linux system packager
written in python2. Determinism here means that produced output should have the
same SHA256 regardless of CPU, CPU architecture, operating system or the
phase of the moon. Unfortunately, this motivation for the project remains to be
unsolved. The project was started in 2014, so things are old. Also, there
is no proper init yet (and systemd is definitely not default).

Key features:
 * simple build framework that provides files and enforces step-by-step script 
 * hash-based caching; same thing is not executed twice
 * offline friendly, uses only host curl to download source packages
 * does not require root access on host
 * does not require Linux or x86 to work (MacOS has worked, but is untested)
 * aims for determinism (a few problems remain)
 * aims to avoid GPL

Limu starts by compiling qemu for host along with other tools (cpio, squashfs,
libarchive) needed to modify Debian CD image to act as a build environment.
Debian was chosen for size (566MB) and it is very trusted source for an
executable binary blob. The modified CD image is used to compile
linux-from-scratch (LFS) environment initally for i386. After a lot of
compilation, cross-compilation and booting, limu gives a x86-64 Linux system
with from chosen source packages.

Getting it running
------------------

Limu needs about 50 GB of free disk space, python2 and a C compiler. Although
not guaranteed, limu shouldn't write outside limu's root directory. Steps:

Dependencies on Ubuntu:
  sudo apt-get install build-essential libglib2-dev ...

Install lpack to ./bin/, it's limu's deterministic tar tool:
  python2 install\_lpack.py

Build rootfs, initrd and kernel to boot x86-64 (can take a day):
  python2 desktop.py

After this you should get a hash for final package. Run:
  tar xvf packages/<sha256>.tar.gz
  ./run\_image\_in\_qemu.sh

You should now have x86-64 with Xorg, fluxbox (WM), xterm and dillo (browser)
running inside qemu that has been booted only by using Debian Rescue CD image
and a bunch source code.

Getting started with code
-------------------------

File ./desktop.py is pretty self-explaining, it orchestrates what should
happen. It uses compilation chains from ./chains/ to get various sets of
software built. ./builders/ directory contains instructions to compile specific
source packages. ./executors/ directory contains executors that are responsible
for executing steps given by builders. ./core/ contains shared code for chains,
builders and executors. Currently three executors exist: host, qemu\_debian and
qemu\_builder. host runs on host and builds qemu and a few other tools.
qemu\_debian uses Debian image to build the first LFS build system.
qemu\_builder uses built LFS system to build more packages and systems.

Determinism
-----------

Determinstic binaries is the main goal of the project. This would solve a lot
of trust issues with binaries, source-only dependency tracking and being
able to reproduce compilation and software issues. It should be
unacceptable that software stack relies on untrusted binaries. Here we
trust only on Debian CD image (and host C compiler) and everything else is XXX auditable.

The idea solve determinism is by running everything inside qemu CPU emulation.
This is slow, but a necessity to not have the host influence on the
execution. There are a few issues with this approach.

Linux makes it very difficult to operate without seeding RNG from natural
sources. This needs more investigation, but simply stuffing entropy to
/dev/random doesn't seem to be enough and the emulation gets stuck. There might
be some protection against this, which needs more investigation.

Compute date needs to remain cBuild scripts seem to constantly misbehave or get into infinite loop if RTC is
funky. This might need 

The execution is insanely slow, however, since the execution is deterministic,
one execution doesn't need to be executed twice. Global caches can be used and
verified from trusted sources.
