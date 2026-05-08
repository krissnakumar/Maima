
#!/bin/bash

# Define paths
PROJECT_DIR=$(pwd)
ICON_PATH="$PROJECT_DIR/maima/assets/logo.png"
EXEC_PATH="$PROJECT_DIR/run.sh"
DESKTOP_FILE="$HOME/.local/share/applications/maima.desktop"

echo "🚀 Creating Linux Mint Desktop Launcher..."

# Create the .desktop file
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=Maima
Comment=Premium Screen Capture Utility
Exec=$EXEC_PATH
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Office;
StartupNotify=true
EOF

# Make everything executable
chmod +x "$EXEC_PATH"
chmod +x "$DESKTOP_FILE"

echo "✅ Success! Maima is now in your Application Menu."
echo "You can search for 'Maima' in your Start Menu and pin it to your panel."
