#!/bin/bash

# AWA Language 安裝腳本
# 支援：Linux (apt), Termux (pkg), macOS (brew)
# 注意：Windows 請用 WSL

set -e

echo "========================================="
echo "AWA Language 安裝腳本"
echo "========================================="

# 偵測系統
detect_os() {
    if [ -n "$TERMUX_VERSION" ]; then
        echo "termux"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        case $ID in
            debian|ubuntu|linuxmint|pop|elementary)
                echo "debian"
                ;;
            fedora|centos|rhel)
                echo "fedora"
                ;;
            arch|manjaro)
                echo "arch"
                ;;
            alpine)
                echo "alpine"
                ;;
            *)
                echo "unknown"
                ;;
        esac
    elif [ "$(uname)" = "Darwin" ]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "偵測到系統: $OS"

# 安裝系統套件
install_packages() {
    case $OS in
        termux)
            echo "安裝 Termux 套件..."
            pkg update
            pkg install -y python nodejs openjdk-21 gcc g++ rust golang mono ruby git make cmake autoconf automake bison flex texinfo
            ;;
        debian)
            echo "安裝 Debian/Ubuntu 套件..."
            sudo apt update
            sudo apt install -y python3 python3-pip openjdk-21-jdk gcc g++ nodejs rustc cargo golang-go mono-complete ruby git make cmake autoconf automake bison flex texinfo
            ;;
        fedora)
            echo "安裝 Fedora 套件..."
            sudo dnf install -y python3 python3-pip java-21-openjdk-devel gcc gcc-c++ nodejs rust cargo golang mono-complete ruby git make cmake autoconf automake bison flex texinfo
            ;;
        arch)
            echo "安裝 Arch 套件..."
            sudo pacman -Syu --noconfirm python python-pip jdk21-openjdk gcc nodejs rust go mono ruby git make cmake autoconf automake bison flex texinfo
            ;;
        macos)
            echo "安裝 macOS 套件..."
            if ! command -v brew >/dev/null 2>&1; then
                echo "請先安裝 Homebrew: https://brew.sh"
                exit 1
            fi
            brew install python openjdk@21 gcc nodejs rust go mono ruby git make cmake autoconf automake bison flex texinfo
            ;;
        alpine)
            echo "安裝 Alpine 套件..."
            apk add python3 py3-pip openjdk21 gcc g++ nodejs rust cargo go mono ruby git make cmake autoconf automake bison flex texinfo
            ;;
        *)
            echo "不支援的系統，請手動安裝以下套件："
            echo "Python 3, Java JDK 21, GCC, G++, Node.js, Rust, Go, Mono, Ruby, Git, make, cmake, autoconf, automake, bison, flex, texinfo"
            echo "然後繼續執行 pip install msgpack"
            ;;
    esac
}

install_packages

# Python 套件
echo "安裝 Python 套件..."
pip install msgpack

# TypeScript
if command -v npm >/dev/null 2>&1; then
    echo "安裝 TypeScript..."
    npm install -g typescript
else
    echo "npm 未安裝，跳過 TypeScript"
fi

# INTERCAL 安裝 (使用預編譯的 deb)
install_intercal() {
    if [ "$OS" = "termux" ]; then
        if [ -f "intercal-deb.deb" ]; then
            echo "安裝 INTERCAL (Termux) from intercal-deb.deb..."
            dpkg -i intercal-deb.deb
            apt-get install -f -y
        else
            echo "找不到 intercal-deb.deb，跳過 INTERCAL 安裝"
            echo "如果你需要 INTERCAL，請手動下載或編譯"
        fi
    elif [ "$OS" = "debian" ] || [ "$OS" = "ubuntu" ]; then
        if [ -f "intercal-deb.deb" ]; then
            echo "安裝 INTERCAL (Linux) from intercal-deb.deb..."
            sudo dpkg -i intercal-deb.deb
            sudo apt-get install -f -y
        else
            echo "找不到 intercal-deb.deb，嘗試從原始碼編譯..."
            compile_intercal
        fi
    else
        echo "非 Debian/Termux 系統，嘗試從原始碼編譯 INTERCAL..."
        compile_intercal
    fi
}

compile_intercal() {
    if command -v git >/dev/null 2>&1; then
        echo "下載 INTERCAL 原始碼..."
        git clone https://github.com/TryItOnline/intercal.git || true
        cd intercal
        echo "編譯 INTERCAL..."
        autoreconf -ivf
        ./configure
        make
        if [ "$OS" = "termux" ]; then
            make install
        else
            sudo make install
        fi
        cd ..
    else
        echo "git 未安裝，跳過 INTERCAL"
    fi
}

install_intercal

# 設定執行檔
echo "設定 AWA 執行檔..."
if [ "$OS" = "termux" ]; then
    mkdir -p $PREFIX/bin
    cat > $PREFIX/bin/awa << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
python3 -m awa "$@"
EOF
    chmod +x $PREFIX/bin/awa
else
    if [ -d "/usr/local/bin" ]; then
        sudo tee /usr/local/bin/awa > /dev/null << 'EOF'
#!/bin/sh
python3 -m awa "$@"
EOF
        sudo chmod +x /usr/local/bin/awa
    else
        mkdir -p ~/.local/bin
        cat > ~/.local/bin/awa << 'EOF'
#!/bin/sh
python3 -m awa "$@"
EOF
        chmod +x ~/.local/bin/awa
        echo "請將 ~/.local/bin 加入 PATH"
    fi
fi

echo "========================================="
echo "AWA Language 安裝完成！"
echo "========================================="
echo ""
echo "使用方式："
echo "  python -m awa 你的程式.awa"
echo "  或"
echo "  awa 你的程式.awa"
echo ""
echo "測試："
echo "  echo 'good morning compiler' > test.awa"
echo "  echo 'say \"Hello from AWA\"' >> test.awa"
echo "  echo 'thank u and goodbye' >> test.awa"
echo "  awa test.awa"
echo ""
echo "注意："
echo "- 所有程式必須以 'good morning compiler' 開頭"
echo "- 所有程式必須以 'thank u and goodbye' 結尾"
echo "- 記得加 please，不然會被罵"