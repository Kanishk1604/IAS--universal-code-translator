# Code Translator

A Python-based code translator that converts code written in **Python** into **JavaScript**. The tool uses Python's `ast` module to parse the input code and translates it into equivalent JavaScript syntax.

---

## Features

- **Translate Python to JavaScript**:
  - Classes
  - Functions
  - If-Else Statements
  - Loops (`for`, `while`)
  - F-strings → JavaScript Template Literals
- **Pluggable Architecture**:
  - Easily extensible to support other programming languages.
- **Error Handling**:
  - Identifies unsupported syntax and outputs comments like `// Unsupported expression`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-translator.git
   cd code-translator
