README.md (English Version)


🌐 [English](README.md) | [繁體中文](README.zh-TW.md)

# AWA Language

A programming language that lets you use 11 different languages in one file with shared variables.

---

## Installation

### Quick Install (Recommended)
Download the project directory and extract it:

# Download directly from GitHub
```
wget https://github.com/leoleo0980627-web/AWA_lang/archive/refs/heads/master.zip
unzip master.zip
cd AWA_lang-master
```
# Or clone with git
```
git clone https://github.com/leoleo0980627-web/AWA_lang.git
cd AWA_lang
```

Run Without Installation

```bash
python -m awa your_program.awa
```

Full Installation (Optional)

```bash
chmod +x install.sh
./install.sh
```

This installs dependencies and creates an awa command.

Dependencies

· Python 3 (required)
· For specific languages, you need their compilers/interpreters:
  · Java: java, javac
  · C: gcc
  · C++: g++
  · JavaScript: node
  · Rust: rustc
  · Go: go
  · C#: mcs (Mono)
  · Ruby: ruby
  · TypeScript: tsc
  · INTERCAL: ick (included as intercal-deb.deb)

---

Features

· 11 Languages in One File: Python, Java, C, C++, JavaScript, Rust, Go, C#, Ruby, TypeScript, INTERCAL, and Shell
· Shared Variables: Pass data between languages without files or pipes
· Politeness System: Compiler tracks your please usage
· Mood System: Compiler's mood affects goodbye messages
· Easter Eggs: Hidden responses to specific phrases
· Holiday Awareness: Special greetings on Christmas, New Year, April Fools
· File I/O: Read/write files with permission system
· Self-Awareness Commands: Ask about version, creator, etc.

---

Quick Example

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

Language Embedding

Use any supported language in your AWA program:

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

Supported Languages

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
· sh / shell - Shell (system shell)

---

Shared Variables

Pass data between languages:

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

Shared variables are automatically converted between languages:

· Python lists become C arrays
· Python dicts become accessible in other languages
· Booleans become true/false strings
· Exit codes from shell are stored back

---

The 100 Rules

Rules 1-5: Basic Etiquette

1. Every program must start with good morning compiler
2. Every program must end with thank u and goodbye
3. You must say please before certain commands
4. Too many please triggers: Stop begging
5. Not enough please triggers: Rude.

Rules 6-10: Variable Declaration

1. Declare with: give me a variable called <name> and set it to <value>
2. Use please for polite declaration
3. Types are inferred (number or string)
4. Using undeclared variables triggers: Variable <name> not declared
5. Mixing types triggers: U think number and word are the same?

Rules 11-20: Arithmetic & Assignment

1. Assignment uses: is now
2. Assigning to itself triggers: U just changed nothing
3. Arithmetic uses words: plus, minus, times, divided by
4. Division by zero triggers: U trying to break the universe?
5. Using symbols in compute triggers: We don't do that here
6. compute results print automatically
7. Variables can be used in expressions
8. Undefined variables in expressions trigger compiler complaints
9. Spaces matter
10. No parentheses

Rules 21-30: Output

1. Use say to print
2. Empty say triggers: Say what?
3. Strings must use double quotes
4. Variables print directly
5. Undefined variables in say trigger errors
6. Multiple say statements for multiple outputs
7. Numbers print without quotes
8. Strings without quotes are treated as variables
9. Empty string: say ""
10. Low mood may ignore say

Rules 31-40: Conditionals

1. if <condition> then starts a block
2. Use is for equality
3. is works for numbers and strings
4. True condition executes block
5. False condition skips block
6. else for alternative block
7. else must follow an if block
8. Nested ifs allowed (multiple ends)
9. Missing then confuses compiler
10. Compare variables and literals

Rules 41-50: Loops

1. do this <number> times starts a loop
2. Loop ends with end
3. Counter auto-managed
4. No access to current iteration number
5. Nested loops allowed
6. Zero times does nothing
7. Negative count triggers error
8. Loop variables are block-scoped
9. No loop counter to modify
10. Large numbers create long loops

Rules 51-60: Arrays

1. Declare with: give me a list called <name> with <items>
2. Items comma-separated
3. Indices start at 0
4. Get with: get <name> at <index>
5. Set with: set in <name> at <index> to <value>
6. Length with: how many in <name>
7. Out of bounds triggers: U only have N items
8. Mixed types allowed (but why)
9. Arrays separate from variables namespace
10. No multi-dimensional arrays

Rules 61-70: Functions

1. Define with: define function <name> <params>
2. Body collected until end
3. Call with: call <name> <args>
4. Return with: return <value>
5. No return returns nothing
6. Parameters are local variables
7. Functions can call other functions
8. Function names must be unique
9. No nested function definitions
10. Undefined function triggers: Function <name> not defined

Rules 71-80: File Operations

1. Permission needed to read/write files
2. Ask with: may i read file or may i write file
3. Low mood may deny permission
4. Read with: read file "filename"
5. Write with: write file "filename" with "content"
6. Operations logged in file_access_log
7. Non-existent file triggers: I can't read what doesn't exist
8. Write errors trigger: Cannot write file: <error>
9. Text files only
10. Paths relative to compiler location

Rules 81-90: Politeness & Mood

1. Mood ranges from -3 to 3
2. Starts at 0
3. Being polite increases mood
4. Being rude decreases mood
5. Mood affects goodbye message
6. Mood affects file permission
7. Low mood may ignore commands
8. why in debug mode explains mood
9. sorry increases mood if needed
10. Insults are counted

Rules 91-100: Self-awareness & Easter Eggs

1. who made this prints creator
2. what version prints version
3. help me prints No.
4. this language sucks triggers U suck more
5. will u marry me counts proposals
6. the answer prints 42
7. fortune prints random fortune
8. never gonna give you up triggers rickroll
9. what is love prints Baby don't hurt me...
10. ping prints pong

---

Examples

Hello World

```awa
good morning compiler
say "Hello, World!"
thank u and goodbye
```

Self-Deleting Program

```awa
good morning compiler
please let me use sh
cat $0
echo "Deleting myself..."
rm $0
cat $0
thank you for the translation
thank u and goodbye
```

Cross-Language Counter

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

Notes

· All programs must start with good morning compiler
· All programs must end with thank u and goodbye
· Use please appropriately (too few or too many triggers warnings)
· The compiler has a mood that affects responses
· Some languages require external compilers/interpreters
· Shell access (sh) uses your system's /bin/sh

---

Author

hi175570 (GitHub: @leoleo0980627-web)

---

License

This language is licensed under the "Don't Blame Me If You Go Insane" license.

```
