#!/bin/bash
set -e
set -x

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing system dependencies..."
sudo apt install --no-install-recommends \
    xserver-xorg xinit x11-xserver-utils unclutter \
    python3-pygame python3-numpy python3-dev git \
    plymouth -y

echo "🧠 Creating .xinitrc to launch ad viewer (pulls latest code)..."
cat <<EOF > ~/.xinitrc
#!/bin/bash
unclutter -idle 0 &
cd ~/freshlux
git pull --quiet
python3 main.py >> ~/freshlux/log.txt 2>&1
EOF
chmod +x ~/.xinitrc

echo "🚀 Enabling GUI on tty1..."
BASH_PROFILE=~/.bash_profile
AUTOLOGIN_LINE='if [ -z "\$DISPLAY" ] && [ \$(tty) = /dev/tty1 ]; then startx; fi'
grep -qxF "$AUTOLOGIN_LINE" "$BASH_PROFILE" || echo "$AUTOLOGIN_LINE" >> "$BASH_PROFILE"

echo "🎨 Installing custom Plymouth splash..."
sudo mkdir -p /usr/share/plymouth/themes/freshlux
sudo cp freshlux.png /usr/share/plymouth/themes/freshlux/logo.png

# freshlux.plymouth
sudo tee /usr/share/plymouth/themes/freshlux/freshlux.plymouth > /dev/null <<EOF
[Plymouth Theme]
Name=FreshLux
Description=Boot splash with FreshLux logo
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/freshlux
ScriptFile=/usr/share/plymouth/themes/freshlux/freshlux.script
EOF

# freshlux.script
sudo tee /usr/share/plymouth/themes/freshlux/freshlux.script > /dev/null <<EOF
theme.image_path = "/usr/share/plymouth/themes/freshlux";
logo = Image("logo.png");
logo:SetZ(100);
logo:MoveTo((Window.GetWidth() - logo:GetWidth()) / 2,
            (Window.GetHeight() - logo:GetHeight()) / 2);
Window.SetBackgroundTopColor(0, 0, 0);
Window.SetBackgroundBottomColor(0, 0, 0);
EOF

echo "🎯 Applying splash..."
sudo plymouth-set-default-theme -R freshlux

echo "🔧 Ensuring splash shows at boot..."
sudo sed -i 's/$/ quiet splash logo.nologo/' /boot/cmdline.txt

echo "🔁 Regenerating initramfs..."
sudo update-initramfs -u

echo "✅ Setup complete. Rebooting in 5 seconds..."
sleep 5
sudo reboot
