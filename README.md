# Obsidian2Anki

A command-line tool that converts Markdown files containing flashcard-style content into CSV files compatible with [Anki](https://apps.ankiweb.net/).
Supports simplified Markdown (headings, bold, italics), LaTeX (inline and block math), and custom separators.

---

## ✨ Features

- Converts Markdown to CSV for Anki import
- Supports **multi-line** questions and answers
- Supports:
  - `**bold**`, `*italic*`
  - `#`, `##`, `###` headers
  - LaTeX: `$...$`, `$$...$$`
- Converts line breaks (`\n`) to `<br>`
- Custom separator between question and answer in `.md` file


## 📦 Requirements

- Python 3.10+
- No external dependencies

---

## ⚙️ Usage

###  📁 Required File Structure

Your input Markdown file should be structured like this:

```markdown
# Question (you can add anything after 'Question' in the header, e.g. number or ID)
What is the capital of France?
:::
Paris

# Question 123
What does HTTP stand for?
:::
HyperText Transfer Protocol
```
**You can use any string instead of `:::` as a separator** (e.g. `???`, `===`, etc.)


### ▶️ Run
```bash
python main.py path/to/input.md output.csv ":::"
```

### 📥 Arguments

| Argument    | Description                                |
| ----------- | ------------------------------------------ |
| `md_path`   | Path to the input `.md` file               |
| `csv_name`  | Output `.csv` file name/path               |
| `separator` | Line used to separate question from answer |

---

## 📂 Project Structure
```
Obsidian2Anki/
├── src/
│   └── converter.py        # Markdown to CSV parser
├── .gitignore
├── out.csv                 # Example output file (optional)
├── pyproject.toml          # Project configuration (e.g. for Ruff, Mypy, etc.)
├── README.md               # Main project description
├── RPis.md                 # (Optional) additional notes or report
├── uv.lock                 # Dependency lock file (from uv/rye)
└── main.py                 # CLI entry point
```
