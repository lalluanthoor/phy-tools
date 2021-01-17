# phy-tools
Installation kit for material simulation tools. Currently supports:
- VASP

In progress:
- Siesta
- Quantum ESPRESSO

## How to use this tool

### Prerequisites
It is only tested with Ubuntu 18.04 and Python 3. Rest of the platforms may or may not work.

### Steps to install
```bash
sudo apt install -y python3-pip
pip3 install virtualenv
git clone https://github.com/lalluanthoor/phy-tools.git
cd phy-tools
python3 -m virtualenv venv
. venv/bin/activate
pip3 install .
phy-tools --help
```
