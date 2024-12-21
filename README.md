# Requirement

To use this project, you need to install Docker & docker-compose (already packed with Docker on windows)

## For Windows :
https://docs.docker.com/desktop/setup/install/windows-install/

## For Linux :

Steps for Ubuntu

### Step 1 : Install Docker

```bash
sudo apt update
sudo apt upgrade -y

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install docker-ce -y

sudo systemctl status docker

sudo usermod -aG docker $USER
newgrp docker
```

Now Docker-compose

### Step 2 : Install Docker-compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```




# Installation

1. To setup the environnement, make sure to install miniconda https://docs.anaconda.com/miniconda/miniconda-install/
2. Create your python environnement
```
conda create -y -n my_env python=3.11
conda activate my_env
pip install pdm ruff==0.3.3 pre-commit
```
3. Go to your folder and install the packages using **pdm**. Initialize the project if needed
```
cd ~/your_work_folder
pdm install --dev
```
