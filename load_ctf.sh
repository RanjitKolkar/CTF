#!/bin/bash

echo "[+] Loading Digital Forensics CTF (Exam Mode)..."
sleep 1

# -------------------------------
# Environment Checks
# -------------------------------
REQUIRED_CMDS=("base64" "rev" "strings" "file" "grep")

for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "[!] Required command '$cmd' not found."
        echo "[!] Please install coreutils / binutils and retry."
        exit 1
    fi
done

# Check attr / setfattr
if ! command -v setfattr &> /dev/null; then
    echo "[!] 'setfattr' not found."
    echo "[+] Installing attr package..."
    sudo apt update && sudo apt install attr -y || {
        echo "[!] Failed to install attr. Contact instructor."
        exit 1
    }
fi

# -------------------------------
# Create Challenge Structure
# -------------------------------
BASE_DIR="forensics_ctf"

mkdir -p "$BASE_DIR"/{challenge1,challenge2,challenge3,challenge4,challenge5}

# -------------------------------
# Challenge 1 – Hidden + Permission
# -------------------------------
echo "FLAG{hidden_files_are_not_secure}" > "$BASE_DIR/challenge1/.cache.tmp"
chmod 111 "$BASE_DIR/challenge1/.cache.tmp"

# -------------------------------
# Challenge 2 – Fake File Type
# -------------------------------
echo -e "\x50\x4b\x03\x04FLAG{extensions_can_lie}" > "$BASE_DIR/challenge2/report.txt"

# -------------------------------
# Challenge 3 – Deleted but Recoverable
# -------------------------------
echo "xxxxFLAG{deleted_does_not_mean_destroyed}xxxx" > "$BASE_DIR/challenge3/disk.img"
sync
rm "$BASE_DIR/challenge3/disk.img"

# -------------------------------
# Challenge 4 – Metadata Evidence
# -------------------------------
echo "evidence" > "$BASE_DIR/challenge4/image.jpg"
setfattr -n user.comment -v "FLAG{metadata_never_lies}" "$BASE_DIR/challenge4/image.jpg"

# -------------------------------
# Challenge 5 – Encoded + Reversed
# -------------------------------
ENC=$(echo -n "FLAG{layers_of_obfuscation}" | base64 | rev)
echo "$ENC" > "$BASE_DIR/challenge5/notes.log"

# -------------------------------
# Validation Checks
# -------------------------------
ERROR=0

[ -d "$BASE_DIR/challenge1" ] || ERROR=1
[ -f "$BASE_DIR/challenge2/report.txt" ] || ERROR=1
[ ! -f "$BASE_DIR/challenge3/disk.img" ] || ERROR=1
getfattr "$BASE_DIR/challenge4/image.jpg" &> /dev/null || ERROR=1
[ -f "$BASE_DIR/challenge5/notes.log" ] || ERROR=1

if [ "$ERROR" -ne 0 ]; then
    echo "[!] One or more challenges failed to load."
    echo "[!] Please contact the instructor."
    exit 1
fi

# -------------------------------
# Success Message
# -------------------------------
echo "[✓] All 5 challenges loaded successfully."
echo "[✓] Navigate to '$BASE_DIR/' to begin analysis."

# -------------------------------
# Self Destruct
# -------------------------------
echo "[!] Cleaning loader file..."
rm -- "$0"
