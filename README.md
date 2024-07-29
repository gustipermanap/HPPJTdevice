setelah login

```python
sudo raspi-config
```

setelah semua di enable

```python
sudo apt-get install -y python3-picamera python3-pip ffmpeg ufw i2c-tools python3-smbus python3-pip
```

setelah keperluan apt di install lalu keperlian pip

```python
sudo pip3 install adafruit-blinka ****adafruit-circuitpython-mlx90614 **smbus2 mlx90614**
```

lalu enable firewall

```python
sudo ufw allow 8000/tcp
```

atau install git dan clone

```python
sudo raspi-config
```

setelah enable semua config

```python
git clone https://github.com/gustipermanap/HPPJTdevice.git .
```

lalu

```python
chmod +x hepi.sh
```

```python
./hepi.sh
```

add network wifi

```jsx
network={
        ssid="Chloride"
        psk="Gusti123"
}

```

```jsx
sudo systemctl restart networking
```
