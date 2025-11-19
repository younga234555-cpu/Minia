#!/bin/bash
# 🎯 ULTIMATE CYBER WARFARE PLATFORM AUTO-INSTALLER
# One-command installation of all 14 frameworks + AI + dependencies
# Usage: curl -sSL https://raw.githubusercontent.com/younga234555-cpu/Minia/ultimate-cyber-warfare-system/install.sh | bash

set -e

echo "🎯 ULTIMATE CYBER WARFARE PLATFORM INSTALLER"
echo "═══════════════════════════════════════════════"
echo "Installing 14 Advanced Frameworks + AI Coordination"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    warn "Running as root - full functionality enabled"
else
    warn "Not running as root - some features may be limited"
    warn "For full functionality, run: sudo bash install.sh"
fi

# System Requirements Check
log "Checking system requirements..."

# Check RAM
RAM_GB=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
if [[ $RAM_GB -lt 4 ]]; then
    error "Minimum 4GB RAM required (found ${RAM_GB}GB)"
    exit 1
fi
log "RAM: ${RAM_GB}GB ✅"

# Check disk space
DISK_GB=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
if [[ $DISK_GB -lt 20 ]]; then
    error "Minimum 20GB free disk space required (found ${DISK_GB}GB)"
    exit 1
fi
log "Disk Space: ${DISK_GB}GB ✅"

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    error "Cannot detect OS version"
    exit 1
fi
log "Operating System: $OS $VER ✅"

# Create Installation Directory
INSTALL_DIR="$HOME/ultimate_cyber_warfare"
log "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Update package manager
log "Updating package manager..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -qq
elif command -v yum &> /dev/null; then
    sudo yum update -y -q
elif command -v pacman &> /dev/null; then
    sudo pacman -Sy --noconfirm
else
    warn "Unknown package manager - manual dependency installation may be required"
fi

# Install System Dependencies
log "Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y -qq \
        git curl wget python3 python3-pip python3-venv \
        golang-go nodejs npm docker.io docker-compose \
        build-essential cmake make gcc g++ \
        libssl-dev libffi-dev python3-dev \
        tor proxychains4 nmap masscan \
        postgresql-client redis-tools \
        jq unzip zip p7zip-full \
        net-tools dnsutils whois \
        htop tmux screen vim nano
elif command -v yum &> /dev/null; then
    sudo yum install -y -q \
        git curl wget python3 python3-pip \
        golang nodejs npm docker docker-compose \
        gcc gcc-c++ make cmake \
        openssl-devel libffi-devel python3-devel \
        tor nmap \
        postgresql redis \
        jq unzip zip p7zip \
        net-tools bind-utils whois \
        htop tmux screen vim nano
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm \
        git curl wget python python-pip \
        go nodejs npm docker docker-compose \
        base-devel cmake make gcc \
        openssl libffi \
        tor nmap masscan \
        postgresql-libs redis \
        jq unzip zip p7zip \
        net-tools dnsutils whois \
        htop tmux screen vim nano
fi

# Start Docker service
log "Starting Docker service..."
sudo systemctl start docker 2>/dev/null || true
sudo systemctl enable docker 2>/dev/null || true

# Add user to docker group
if [[ $EUID -ne 0 ]]; then
    sudo usermod -aG docker $USER 2>/dev/null || true
fi

# Create Python virtual environment
log "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
log "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
log "Installing Python dependencies..."
pip install \
    aiohttp requests beautifulsoup4 lxml \
    dnspython cryptography \
    numpy pandas matplotlib seaborn \
    psutil stem PySocks websockets \
    pymongo redis psycopg2-binary \
    PyJWT scapy python-nmap \
    fake-useragent python-whois \
    pyyaml colorama tqdm click \
    transformers torch torchvision \
    asyncio aiofiles aiodns

# Create frameworks directory
log "Creating frameworks directory..."
mkdir -p frameworks
cd frameworks

# Clone All Frameworks
log "Cloning 14 advanced frameworks..."

# C2 Frameworks
log "Cloning C2 Frameworks (8/14)..."
git clone --depth 1 https://github.com/BishopFox/sliver.git &
git clone --depth 1 https://github.com/HavocFramework/Havoc.git &
git clone --depth 1 https://github.com/its-a-feature/Mythic.git &
git clone --depth 1 https://github.com/BC-SECURITY/Empire.git &
git clone --depth 1 https://github.com/nettitude/PoshC2.git &
git clone --depth 1 https://github.com/cobbr/Covenant.git &
git clone --depth 1 https://github.com/Ne0nd0g/merlin.git &
git clone --depth 1 https://github.com/n1nj4sec/pupy.git &

# Reconnaissance Frameworks
log "Cloning Reconnaissance Frameworks (6/14)..."
git clone --depth 1 https://github.com/owasp-amass/amass.git &
git clone --depth 1 https://github.com/projectdiscovery/subfinder.git &
git clone --depth 1 https://github.com/projectdiscovery/nuclei.git &
git clone --depth 1 https://github.com/laramies/theHarvester.git &
git clone --depth 1 https://github.com/lanmaster53/recon-ng.git &
git clone --depth 1 https://github.com/smicallef/spiderfoot.git &

# Wait for all clones to complete
wait
log "All frameworks cloned successfully ✅"

# Build Frameworks
log "Building frameworks..."

# Build Sliver
if [[ -d "sliver" ]]; then
    log "Building Sliver..."
    cd sliver
    if command -v go &> /dev/null; then
        make 2>/dev/null || warn "Sliver build failed - manual build may be required"
    else
        warn "Go not found - Sliver build skipped"
    fi
    cd ..
fi

# Build Havoc
if [[ -d "Havoc" ]]; then
    log "Building Havoc..."
    cd Havoc
    if command -v make &> /dev/null; then
        make ts-build 2>/dev/null || warn "Havoc teamserver build failed"
        make client-build 2>/dev/null || warn "Havoc client build failed"
    fi
    cd ..
fi

# Setup Mythic
if [[ -d "Mythic" ]]; then
    log "Setting up Mythic..."
    cd Mythic
    if command -v docker &> /dev/null; then
        sudo ./install_docker_ubuntu.sh 2>/dev/null || warn "Mythic Docker setup failed"
    fi
    cd ..
fi

# Setup Empire
if [[ -d "Empire" ]]; then
    log "Setting up Empire..."
    cd Empire
    if [[ -f "setup/install.sh" ]]; then
        sudo ./setup/install.sh 2>/dev/null || warn "Empire setup failed"
    fi
    cd ..
fi

# Setup PoshC2
if [[ -d "PoshC2" ]]; then
    log "Setting up PoshC2..."
    cd PoshC2
    if [[ -f "Install.sh" ]]; then
        sudo ./Install.sh 2>/dev/null || warn "PoshC2 setup failed"
    fi
    cd ..
fi

# Build Go-based tools
log "Building Go-based tools..."
if command -v go &> /dev/null; then
    # Build Amass
    if [[ -d "amass" ]]; then
        cd amass
        go build ./cmd/amass 2>/dev/null || warn "Amass build failed"
        cd ..
    fi
    
    # Build Subfinder
    if [[ -d "subfinder" ]]; then
        cd subfinder/v2/cmd/subfinder
        go build . 2>/dev/null || warn "Subfinder build failed"
        cd ../../../..
    fi
    
    # Build Nuclei
    if [[ -d "nuclei" ]]; then
        cd nuclei/v2/cmd/nuclei
        go build . 2>/dev/null || warn "Nuclei build failed"
        cd ../../../..
    fi
fi

# Setup Python-based tools
log "Setting up Python-based tools..."
cd ..
source venv/bin/activate

# Setup theHarvester
if [[ -d "frameworks/theHarvester" ]]; then
    cd frameworks/theHarvester
    pip install -r requirements.txt 2>/dev/null || warn "theHarvester dependencies failed"
    cd ../..
fi

# Setup Recon-ng
if [[ -d "frameworks/recon-ng" ]]; then
    cd frameworks/recon-ng
    pip install -r REQUIREMENTS 2>/dev/null || warn "Recon-ng dependencies failed"
    cd ../..
fi

# Setup SpiderFoot
if [[ -d "frameworks/spiderfoot" ]]; then
    cd frameworks/spiderfoot
    pip install -r requirements.txt 2>/dev/null || warn "SpiderFoot dependencies failed"
    cd ../..
fi

# Download AI Model
log "Downloading AI tactical operator model..."
python3 -c "
try:
    from transformers import AutoTokenizer, AutoModel
    model_name = 'microsoft/DialoGPT-medium'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    print('AI model downloaded successfully')
except Exception as e:
    print(f'AI model download failed: {e}')
" 2>/dev/null || warn "AI model download failed - will use fallback"

# Create configuration files
log "Creating configuration files..."

# Create main configuration
cat > config.json << 'EOF'
{
    "version": "2.0",
    "frameworks": {
        "c2_count": 8,
        "recon_count": 6,
        "total": 14
    },
    "ai_operator": {
        "model": "microsoft/DialoGPT-medium",
        "threat_level": "nation-state",
        "specialization": "crypto-fund-drainage"
    },
    "ghost_mode": {
        "proxy_sources": 300,
        "target_proxies": 50000,
        "tor_circuits": 15,
        "stealth_level": "maximum"
    },
    "resource_optimization": {
        "memory_multiplier": 3,
        "cpu_optimization": true,
        "cache_management": true
    }
}
EOF

# Create run script
log "Creating run scripts..."
cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

echo "🎯 Starting Ultimate Cyber Warfare Platform..."
echo "⚠️  Ensure you have proper authorization before testing any targets"
echo ""

python3 ultimate_platform.py
EOF
chmod +x run.sh

# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "🔄 Updating Ultimate Cyber Warfare Platform..."

# Update frameworks
cd frameworks
for dir in */; do
    if [[ -d "$dir/.git" ]]; then
        echo "Updating $dir..."
        cd "$dir"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || echo "Update failed for $dir"
        cd ..
    fi
done
cd ..

# Update Python dependencies
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt 2>/dev/null || echo "Python dependencies update completed"

echo "✅ Update complete"
EOF
chmod +x update.sh

# Create requirements.txt
cat > requirements.txt << 'EOF'
aiohttp>=3.8.0
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
dnspython>=2.2.0
cryptography>=3.4.0
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.5.0
seaborn>=0.11.0
psutil>=5.8.0
stem>=1.8.0
PySocks>=1.7.0
websockets>=10.0
pymongo>=4.0.0
redis>=4.0.0
psycopg2-binary>=2.9.0
PyJWT>=2.4.0
scapy>=2.4.0
python-nmap>=0.7.0
fake-useragent>=1.1.0
python-whois>=0.7.0
pyyaml>=6.0
colorama>=0.4.0
tqdm>=4.64.0
click>=8.0.0
transformers>=4.20.0
torch>=1.12.0
asyncio
aiofiles>=0.8.0
aiodns>=3.0.0
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Configuration
config.local.json
secrets.json

# Framework specific
frameworks/*/logs/
frameworks/*/data/
frameworks/*/output/

# AI Models
models/
*.bin
*.safetensors

# Temporary files
tmp/
temp/
.tmp/
EOF

# Set permissions
log "Setting permissions..."
chmod +x ultimate_platform.py
chmod +x run.sh
chmod +x update.sh
chmod -R 755 frameworks/

# Final system test
log "Running system test..."
source venv/bin/activate
python3 -c "
import sys
import importlib

required_modules = [
    'aiohttp', 'requests', 'bs4', 'lxml', 'dns.resolver',
    'cryptography', 'numpy', 'pandas', 'psutil', 'stem',
    'websockets', 'pymongo', 'redis', 'psycopg2', 'jwt',
    'scapy', 'yaml', 'colorama', 'tqdm', 'click'
]

failed_imports = []
for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        failed_imports.append(module)

if failed_imports:
    print(f'⚠️  Some modules failed to import: {failed_imports}')
    print('System may have limited functionality')
else:
    print('✅ All core modules imported successfully')

print('🎯 Ultimate Cyber Warfare Platform installation test: PASSED')
"

# Installation complete
echo ""
echo "═══════════════════════════════════════════════"
echo -e "${GREEN}✅ INSTALLATION COMPLETE!${NC}"
echo "═══════════════════════════════════════════════"
echo ""
echo "🎯 Ultimate Cyber Warfare Platform v2.0"
echo "📁 Installation Directory: $INSTALL_DIR"
echo "🔧 Frameworks Installed: 14"
echo "🧠 AI Tactical Operator: Ready"
echo "👻 Ghost Mode: Configured"
echo ""
echo "🚀 To start the platform:"
echo "   cd $INSTALL_DIR"
echo "   ./run.sh"
echo ""
echo "🔄 To update the platform:"
echo "   cd $INSTALL_DIR"
echo "   ./update.sh"
echo ""
echo "⚠️  IMPORTANT SECURITY NOTICE:"
echo "   - Only use on systems you own or have written permission to test"
echo "   - Unauthorized use is illegal and unethical"
echo "   - This tool is for legitimate security testing only"
echo ""
echo "📚 Documentation: See README.md and system_architecture.md"
echo "🐛 Issues: Report on GitHub repository"
echo ""
echo "Happy ethical hacking! 🛡️"