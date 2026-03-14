README.zh-TW.md (繁體中文版)


🌐 [English](README.md) | [繁體中文](README.zh-TW.md)

# AWA 語言

一個可以在同一個檔案裡使用 11 種語言，並且共用變數的程式語言。

---

##安裝方式

### 快速安裝（推薦）
直接下載專案目錄並解壓縮：

# 直接從 GitHub 下載
```
wget https://github.com/leoleo0980627-web/AWA_lang/archive/refs/heads/master.zip
unzip master.zip
cd AWA_lang-master

或用 git 克隆
```
```
git clone https://github.com/leoleo0980627-web/AWA_lang.git
cd AWA_lang
```

不安裝直接執行

```
python -m awa 你的程式.awa
```

完整安裝（選擇性）

```bash
chmod +x install.sh
./install.sh
```

這會安裝依賴套件並建立 awa 指令。

依賴套件

· Python 3（必要）
· 特定語言需要對應的編譯器/直譯器：
  · Java：java、javac
  · C：gcc
  · C++：g++
  · JavaScript：node
  · Rust：rustc
  · Go：go
  · C#：mcs（Mono）
  · Ruby：ruby
  · TypeScript：tsc
  · INTERCAL：ick（已包含 intercal-deb.deb）

---

功能特色

· 11 種語言在同一個檔案：Python、Java、C、C++、JavaScript、Rust、Go、C#、Ruby、TypeScript、INTERCAL、Shell
· 共用變數：在不同語言之間傳遞資料，不用檔案或 pipe
· 禮貌系統：編譯器會計算你用了幾次 please
· 情緒系統：編譯器的情緒會影響道別訊息
· 彩蛋：特定指令會有隱藏回應
· 節日感知：聖誕節、新年、愚人節有特殊問候
· 檔案讀寫：需要權限才能讀寫檔案
· 自我意識指令：可以問版本、作者等

---

快速範例

```awa
good morning compiler

please let me use py
shared.message = "Hello from Python"
shared.numbers = [1, 2, 3, 4, 5]
thank you for the translation

please let me use c
for(int i = 0; i < 5; i++) {
    printf("%d\n", shared.numbers[i]);
}
printf("%s\n", shared.message);
thank you for the translation

thank u and goodbye
```

---

語言嵌入

在 AWA 程式中使用任何支援的語言：

```awa
please let me use python
print("Hello from Python")
thank you for the translation

please let me use c
printf("Hello from C\n");
thank you for the translation

please let me use sh
echo "Hello from shell"
thank you for the translation
```

支援的語言

· py / python - Python
· java - Java
· c - C
· cpp / c++ - C++
· js / javascript - JavaScript (Node.js)
· rust - Rust
· go - Go
· cs / csharp - C# (Mono)
· ruby - Ruby
· ts / typescript - TypeScript
· intercal - INTERCAL
· sh / shell - Shell（系統的 shell）

---

共用變數

在不同語言之間傳遞資料：

```awa
please let me use py
shared.counter = 42
shared.message = "hello"
shared.numbers = [1, 2, 3, 4, 5]
thank you for the translation

please let me use c
for(int i = 0; i < 5; i++) {
    printf("%d\n", shared.numbers[i]);
}
printf("%s %d\n", shared.message, shared.counter);
thank you for the translation

please let me use sh
echo "$SHARED_MESSAGE $SHARED_COUNTER"
for num in $SHARED_NUMBERS; do
    echo $num
done
thank you for the translation
```

共用變數會在不同語言之間自動轉換：

· Python list 變成 C array
· Python dict 可以在其他語言存取
· 布林值變成 true/false 字串
· shell 的 exit code 會存回 shared

---

100 條規則

規則 1-5：基本禮儀

1. 每個程式必須以 good morning compiler 開頭
2. 每個程式必須以 thank u and goodbye 結尾
3. 某些指令前必須加 please
4. 太有禮貌會觸發 Stop begging
5. 不夠禮貌會觸發 Rude.

規則 6-10：變數宣告

1. 用 give me a variable called <名稱> and set it to <值> 宣告
2. 用 please 可以有禮貌地宣告
3. 型態自動推斷（數字或字串）
4. 使用未宣告的變數觸發 Variable <名稱> not declared
5. 混用型態觸發 U think number and word are the same?

規則 11-20：運算與賦值

1. 賦值用 is now
2. 變數賦值給自己觸發 U just changed nothing
3. 算術用單字：plus（加）、minus（減）、times（乘）、divided by（除）
4. 除以零觸發 U trying to break the universe?
5. compute 裡用符號觸發 We don't do that here
6. compute 結果自動印出
7. 變數可在表達式中使用
8. 表達式裡有未定義變數會觸發編譯器抱怨
9. 空格很重要
10. 沒有括號

規則 21-30：輸出

1. 用 say 印出東西
2. say 後面沒東西觸發 Say what?
3. 字串必須用雙引號
4. 變數可以直接印
5. 印不存在的變數會觸發錯誤
6. 多個 say 印多個東西
7. 數字印出來不用引號
8. 沒引號的字串會被當成變數
9. 空字串：say ""
10. 情緒太低可能無視 say

規則 31-40：條件判斷

1. if <條件> then 開始一個區塊
2. 用 is 表示等於
3. is 對數字和字串都有效
4. 條件為真執行區塊
5. 條件為假跳過區塊
6. else 表示否則
7. else 必須在 if 區塊之後
8. 可以巢狀 if（要用多個 end）
9. 忘記 then 會讓編譯器混亂
10. 條件可以比較變數和字面值

規則 41-50：迴圈

1. do this <次數> times 開始迴圈
2. 迴圈用 end 結束
3. 計數器自動管理
4. 無法取得目前是第幾次
5. 可以巢狀迴圈
6. 次數為 0 什麼都不會發生
7. 負的次數會觸發錯誤
8. 迴圈變數是區塊作用域
9. 沒有計數器可以修改
10. 數字太大會跑很久

規則 51-60：陣列

1. 用 give me a list called <名稱> with <項目> 宣告
2. 項目用逗號分隔
3. 索引從 0 開始
4. 用 get <名稱> at <索引> 取得元素
5. 用 set in <名稱> at <索引> to <值> 設定元素
6. 用 how many in <名稱> 取得長度
7. 索引超出範圍觸發 U only have N items
8. 可以混用型態（但為什麼要這樣做）
9. 陣列和變數是分開的命名空間
10. 沒有多維陣列

規則 61-70：函式

1. 用 define function <名稱> <參數> 定義
2. 函式本體直到 end
3. 用 call <名稱> <參數值> 呼叫
4. 用 return <值> 回傳
5. 沒有 return 不回傳東西
6. 參數是區域變數
7. 函式可以呼叫其他函式
8. 函式名稱必須唯一
9. 不能在函式裡定義函式
10. 未定義的函式觸發 Function <名稱> not defined

規則 71-80：檔案操作

1. 需要權限才能讀寫檔案
2. 用 may i read file 或 may i write file 詢問
3. 情緒太低會拒絕
4. 用 read file "檔名" 讀取
5. 用 write file "檔名" with "內容" 寫入
6. 操作會被記錄在 file_access_log
7. 讀取不存在的檔案觸發 I can't read what doesn't exist
8. 寫入錯誤觸發 Cannot write file: <錯誤>
9. 只能讀寫文字檔
10. 路徑相對於執行編譯器的位置

規則 81-90：禮貌與情緒

1. 情緒從 -3 到 3
2. 從 0 開始
3. 有禮貌會增加情緒
4. 沒禮貌會降低情緒
5. 情緒影響道別訊息
6. 情緒影響檔案權限
7. 情緒太低可能無視指令
8. why 在 debug 模式會解釋原因
9. sorry 在需要道歉時會增加情緒
10. 罵人的次數會被記錄

規則 91-100：自我意識與彩蛋

1. who made this 印出作者
2. what version 印出版本
3. help me 印出 No.
4. this language sucks 觸發 U suck more
5. will u marry me 會計算求婚次數
6. the answer 印出 42
7. fortune 印出隨機運勢
8. never gonna give you up 觸發 rickroll
9. what is love 印出 Baby don't hurt me...
10. ping 印出 pong

---

範例

Hello World

```awa
good morning compiler
say "Hello, World!"
thank u and goodbye
```

自殺程式

```awa
good morning compiler
please let me use sh
cat $0
echo "正在刪除自己..."
rm $0
cat $0
thank you for the translation
thank u and goodbye
```

跨語言計數器

```awa
good morning compiler
give me a variable called counter and set it to 0

please let me use py
shared.counter = shared.counter + 1
print(f"Python: {shared.counter}")
thank you for the translation

please let me use c
shared.counter++;
printf("C: %d\n", shared.counter);
thank you for the translation

please let me use sh
SHARED_COUNTER=$((SHARED_COUNTER + 1))
echo "Shell: $SHARED_COUNTER"
thank you for the translation

say "Final count: " counter
thank u and goodbye
```

---

注意事項

· 所有程式必須以 good morning compiler 開頭
· 所有程式必須以 thank u and goodbye 結尾
· 請適當使用 please（太多或太少都會被罵）
· 編譯器有情緒，會影響回應
· 部分語言需要安裝對應的編譯器/直譯器
· Shell 使用系統的 /bin/sh

---

作者

hi175570 (GitHub: @leoleo0980627-web)

---

授權條款

本語言採用「如果你瘋了不要怪我」授權。

```
