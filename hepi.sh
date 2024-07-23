#!/bin/bash
# Skrip untuk menginstal paket dan tools, kemudian mengatur firewall

# Update package list and upgrade all packages
echo "Memperbarui daftar paket..."
sudo apt-get update

# Install required packages
echo "Menginstal paket-paket yang diperlukan..."
sudo apt-get install -y git python3-picamera python3-pip ffmpeg ufw i2c-tools python3-smbus

# Install Python packages using pip
echo "Menginstal paket-paket Python yang diperlukan..."
sudo pip3 install adafruit-blinka adafruit-circuitpython-mlx90614 smbus2 mlx90614

# Allow traffic on port 8000/tcp
echo "Mengizinkan lalu lintas pada port 8000/tcp..."
sudo ufw allow 8000/tcp

echo "Semua tugas telah selesai."
