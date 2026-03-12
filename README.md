📝 雙語 README.md

```markdown
# AWA Language / AWA 語言

**The Most Polite Yet Annoying Programming Language / 最有禮貌但也最機掰的程式語言**

[![GitHub](https://img.shields.io/badge/GitHub-AWA__lang-blue?logo=github)](https://github.com/leoleo0980627-web/AWA_lang)

---

## 📦 Installation / 安裝

### 從 GitHub 克隆 / Clone from GitHub
```bash
git clone https://github.com/leoleo0980627-web/AWA_lang.git
cd AWA_lang
```

依賴安裝 / Install Dependencies

```bash
chmod +x install.sh
./install.sh
```

---

📋 Dependencies / 依賴列表

執行 AWA 需要以下工具 / AWA requires these tools:

語言 / Language 指令 / Command 安裝方式 / Installation
Python 3 python3 apt install python3 / pkg install python
Java javac, java apt install openjdk-21-jdk / pkg install openjdk-21
C gcc apt install gcc / pkg install gcc
C++ g++ apt install g++ / pkg install g++
JavaScript node apt install nodejs / pkg install nodejs
Rust rustc apt install rustc / pkg install rust
Go go apt install golang-go / pkg install golang
C# mcs apt install mono-complete / pkg install mono
Ruby ruby apt install ruby / pkg install ruby
TypeScript tsc npm install -g typescript
INTERCAL ick 手動編譯 / Build from source

Python 套件 / Python packages:

```bash
pip install msgpack
```

---

🚀 Usage / 使用方法

```bash
# 直接執行 / Run directly
python -m awa your_program.awa

# 或使用安裝後的指令 / Or use installed command
awa your_program.awa
```

---

📜 The 100 Mysterious Rules / 100條神秘規則

English Version

Rule 1-5: Basic Etiquette

1. Every program must start with good morning compiler
2. Every program must end with thank u and goodbye
3. You must say please before certain commands
4. If you're too polite, compiler says Stop begging
5. If you're not polite enough, compiler says Rude.

Rule 6-10: Variable Declaration

1. Declare variables with give me a variable called <name> and set it to <value>
2. Use please give me a variable called... for polite declaration
3. Variables types are inferred (number or string)
4. Using undeclared variables triggers Variable <name> not declared
5. Mixing types triggers U think number and word are the same?

[... 其餘規則請參考原始碼 / See source code for complete 100 rules ...]

中文版本

規則 1-5：基本禮儀

1. 每個程式必須以 good morning compiler 開頭
2. 每個程式必須以 thank u and goodbye 結尾
3. 某些指令前必須加 please
4. 太有禮貌會觸發 Stop begging（別再求了）
5. 不夠禮貌會觸發 Rude.（沒禮貌）

規則 6-10：變數宣告

1. 用 give me a variable called <名稱> and set it to <值> 宣告變數
2. 用 please give me a variable called... 可以有禮貌地宣告
3. 變數型態自動推斷（數字或字串）
4. 使用未宣告的變數觸發 Variable <名稱> not declared
5. 混用型態觸發 U think number and word are the same?

---

✨ Features / 特色

· 🗣️ Must greet the compiler / 必須跟編譯器打招呼
· 😤 Politeness counter / 禮貌計數器（太少太多都會被罵）
· 🌐 11 languages embedded / 11種語言嵌入
  · Python, Java, JavaScript, C, C++, Rust, Go, C#, Ruby, TypeScript, INTERCAL
· 💾 Cross-language shared storage / 跨語言共享儲存
· 😡 Mood system / 情緒系統（影響 goodbye 訊息）
· 🎮 Easter eggs / 彩蛋（the answer, fortune, never gonna give you up...）
· 📅 Holiday awareness / 節日感知（聖誕節、新年、愚人節）

---

📁 Project Structure / 專案結構

```
awa/
├── __init__.py
├── __main__.py
├── awa.py                 # 主程式
├── core/                   # 核心功能
│   ├── compiler.py
│   ├── executor.py
│   ├── politeness.py
│   └── scope.py
├── lang/                   # 語言處理器
│   ├── python.py
│   ├── java.py
│   ├── c.py
│   └── ... (11 languages)
├── shared/                 # 共享儲存
│   └── storage.py
├── easter/                 # 彩蛋
│   └── eggs.py
└── utils/                  # 工具
    ├── colors.py
    └── helpers.py
```

---

📝 Example / 範例

```awa
good morning compiler

say "=== Testing All 11 Languages ==="

please let me use py
print("Hello from Python!")
thank you for the translation

please let me use java
System.out.println("Hello from Java!");
thank you for the translation

please let me use c
printf("Hello from C!\\n");
thank you for the translation

the answer
fortune

thank u and goodbye
```

執行結果 / Output:

```
Hello from Python!
Hello from Java!
Hello from C!
42
U will forget a semicolon
Goodbye.
```

---

📜 License / 授權條款

This language is licensed under the "Don't Blame Me If You Go Insane" license.

本語言採用「如果你瘋了不要怪我」授權。

---

👤 Author / 作者

hi175570 (GitHub: @leoleo0980627-web)

---

⚠️ Disclaimer / 免責聲明

使用本語言可能導致：

· 被編譯器罵
· 被編譯器稱讚
· 被編譯器拒絕求婚
· 在聖誕節收到問候
· 莫名其妙印出 42
· 強迫症發作
· 想寫 INTERCAL

作者不承擔任何精神損失責任。

Using this language may cause:

· Being yelled at by compiler
· Being praised by compiler
· Being rejected for marriage by compiler
· Getting Christmas greetings
· Random 42 outputs
· OCD flare-ups
· Urges to write INTERCAL

Author is not responsible for any mental damage.

```

---

## ✅ **特點**

- 雙語（英文 + 中文）
- 神秘規則列出前 10 條（完整 100 條在原始碼）
- 可複製的程式碼框
- 依賴列表表格
- Git clone 指令
- 免責聲明（很重要）
