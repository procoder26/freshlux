#!/bin/bash

set -e
set -x

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing system dependencies..."
sudo apt install --no-install-recommends \
    xserver-xorg xinit x11-xserver-utils unclutter \
    python3-pygame python3-numpy python3-dev git \
    plymouth plymouth-themes -y

echo "📁 Cloning FreshLux repo..."
cd ~
if [ ! -d "freshlux" ]; then
  git clone https://github.com/procoder26/freshlux.git
else
  echo "FreshLux repo already cloned."
fi

echo "🧠 Creating .xinitrc to launch ad viewer..."
cat <<EOF > ~/.xinitrc
#!/bin/bash
unclutter -idle 0 &
python3 ~/freshlux/main.py
EOF
chmod +x ~/.xinitrc

echo "🚀 Setting autostart for tty1 login..."
BASH_PROFILE=~/.bash_profile
AUTOLOGIN_LINE='if [ -z "$DISPLAY" ] && [ $(tty) = /dev/tty1 ]; then startx; fi'
grep -qxF "$AUTOLOGIN_LINE" "$BASH_PROFILE" || echo "$AUTOLOGIN_LINE" >> "$BASH_PROFILE"

echo "🎨 Setting up boot splash with FreshLux logo..."
sudo cp ~/freshlux/freshlux.png /usr/share/plymouth/themes/spinner/freshlux.png

sudo tee /usr/share/plymouth/themes/spinner/spinner.script > /dev/null <<'EOF'
theme.image_path = "/usr/share/plymouth/themes/spinner";
freshlux_logo = Image("freshlux.png");
freshlux_logo:SetZ(10);
freshlux_logo:MoveTo((Window.GetWidth() - freshlux_logo:GetWidth()) / 2, Window.GetHeight() * 0.35);
Window.SetBackgroundTopColor(0, 0, 0);
Window.SetBackgroundBottomColor(0, 0, 0);
spinner = Sprite();
spinner:SetPosition(Window.GetWidth() / 2, Window.GetHeight() * 0.65);
spinner:SetZ(100);
spinner:SetAnimation("spinner", 30);
EOF

echo "📝 Updating plymouth config..."
sudo sed -i 's|^ImageDir=.*|ImageDir=/usr/share/plymouth/themes/spinner|' /usr/share/plymouth/themes/spinner/spinner.plymouth
sudo sed -i 's|^ScriptFile=.*|ScriptFile=/usr/share/plymouth/themes/spinner/spinner.script|' /usr/share/plymouth/themes/spinner/spinner.plymouth

echo "🎯 Setting spinner theme..."
sudo plymouth-set-default-theme spinner

echo "🔧 Updating bootloader config..."
BOOT_CMDLINE="/boot/cmdline.txt"
if ! grep -q "quiet splash logo.nologo" "$BOOT_CMDLINE"; then
  sudo sed -i 's/$/ quiet splash logo.nologo/' "$BOOT_CMDLINE"
fi

echo "🔁 Regenerating initramfs..."
sudo update-initramfs -u

echo "✅ Setup complete. Rebooting in 5 seconds..."
sleep 5
sudo reboot
