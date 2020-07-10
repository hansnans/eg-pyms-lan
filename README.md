# Energenie PMS2-LAN Python Interface

## config

There are two ways to configure the cli module

### commandline
| arg  | desription                                                          |
| ---- | ------------------------------------------------------------------- |
| -H   | host or ip of device to control                                     |
| -p   | port that is configured in the WebUI as _Power Manager client port_ |
|      | default is **5000**                                                 |
| -P   | password that is configured                                         |
|      | default is **1**                                                    |


### config file 

The config is expected in the JSON format.
A template config file is under __conf.json.template__

To use the config file variant just pass only the argument `--config <filename>`

## Install
```
pip install eg_pyms_lan-2.0-py3-none-any.whl
```

## Run

To start the script just run
```bash
pymslan <args> <command> [plug]
```

Configuration arguments as explained above have to be present.
possible commands are:

| command          | desription                             |
| ---------------- | -------------------------------------- |
| enable <plug>    | enable the given plug                  |
| disable <plug>   | disable the given plug                 |
| status           | print the current status of all plugs  |

## Thanks
A big thanks to [zdazzy](https://github.com/zdazzy/) for reverse-engeneering the communication.
