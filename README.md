# PSW_G10
Repo for Project Software (Group 10)


## Instructions for pysense

In case anyone wishes to change the "end device" on TTN, you just need to go the main.py file and edit:
```
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('AED547666A2978DD169E15194F1117F3')
dev_eui = ubinascii.unhexlify('70B3D57ED0049E64')
```
Current API key: 'I3FZTQWGY6GIQ63X3DXR7KGFNSREEUN37OEKQYY'. **This key will change if the device is registered with another application on TTN**
