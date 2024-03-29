# Quick Start Guide

## Создание VM

- Скачайте ISO Ubuntu 22.04 с [ubuntu.com](https://ubuntu.com/download/server).
- В VirtualBox создайте новую VM: выберите Linux -> Ubuntu (64-bit), задайте RAM и размер диска.
- Установите систему, используя скачанный ISO-образ.

## Настройка сети

- Настройте сетевой адаптер в VirtualBox:

  - Откройте настройки виртуальной машины, перейдите в раздел "Сеть" и выберите подходящий режим сетевого адаптера. Например, "Мост" (Bridged Adapter) для получения IP-адреса из вашей локальной сети.
- Откройте или создайте файл конфигурации сети: `sudo nano /etc/netplan/00-installer-config.yaml` и добавьте следующий конфиг:

  ```yaml
  network:
    version: 2
    renderer: networkd
    ethernets:
      enp0s9: # Замените на имя вашего интерфейс !
        dhcp4: no
        addresses: [192.168.3.28/24]
        routes:
          - to: default
            via: 192.168.3.1 # Замените на ваш route. Глянуть можно в ip route show
        nameservers:
          addresses: [8.8.8.8, 8.8.4.4]
  ```
- Примените настройки: `sudo netplan apply`

## Настройка доступа по SSH

- Отредактируйте файл `/etc/ssh/sshd_config`, заменив `PermitRootLogin` на `yes`.
- Перезапустите SSH сервис: `sudo systemctl restart sshd`.
- Измените пароль пользователя root: `passwd`.

## Добавление блочных устройств

- **Добавьте новые виртуальные жесткие диски через VirtualBox:**
  - Остановите виртуальную машину, откройте настройки, перейдите в раздел "Хранилище", выберите контроллер, к которому вы хотите добавить диск, и нажмите на иконку добавления нового диска (синий плюсик у CD/DVD-драйва). Выберите "Создать виртуальный жесткий диск" и следуйте инструкциям мастера.
  - В выводе `lsblk` проверьте, что диски успешно прокинуты.


## Настройка виртуального окружения и установка зависимостей

Чтобы начать работу, сначала необходимо настроить виртуальное окружение и установить все необходимые зависимости.

### Создание виртуального окружения

Выполните следующую команду в терминале:

```bash
python3 -m venv venv
```

Эта команда создаст новое виртуальное окружение в папке `venv`.

### Активация виртуального окружения

Для активации виртуального окружения используйте одну из следующих команд в зависимости от вашей операционной системы:

На Windows:

```bash
.\venv\Scripts\activate
```

На Unix или MacOS:

```bash
source venv/bin/activate
```

### Установка зависимостей

Установите все необходимые зависимости, выполнив следующую команду:

```bash
pip install -r requirements.txt
```

## Запуск тестов

Для запуска тестов воспользуйтесь инструментом `pytest`. Выполните следующую команду:

```bash
python -m pytest tests/your-test-name
```
