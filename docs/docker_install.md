# Установка Docker 

## Windows

Скачать докер и настроить использование по WSL по этой [документации](./docker_to_wsl.md)

## Linux

### 1. Скачивание Docker и Docker Compose

```
sudo apt-get update
sudo apt-get --no-install-recommends install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
sudo apt-get update
sudo apt-get --no-install-recommends install -y \
  docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 2. Добавляем группу Докер, чтобы не писать sudo каждый раз

```
sudo groupadd docker
sudo usermod -aG docker $USER
```