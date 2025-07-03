import re
import csv


def md_to_html(text: str) -> str:
    r"""
    Converts a simplified Markdown + LaTeX string into basic HTML.

     This function replaces:
    - `**bold**` → `<strong>`
    - `*italic*` → `<em>`
    - headers like `#`, `##`, `###` → `<h1>`, `<h2>`, `<h3>`
    - inline math `$...$` → `\\(...\\)`
    - display math `$$...$$` → `\\[...\\]`
    - line breaks (`\\n`) → `<br>`

    Args:
        text (str): Input string in simplified Markdown format, possibly with LaTeX expressions.

    Returns:
        str: The resulting HTML string, safe to embed in Anki or other HTML-based viewers.
    """
    # Changing $$...$$ into \[...\]
    text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)

    # Changing $...$ into \(...\)
    text = re.sub(r"\$(?!\$)(.+?)(?<!\$)\$", r"\\(\1\\)", text)

    # bold: **...** -> <strong>...</strong>
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # italic: *...* -> <em>...</em>
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # headers: ## ... -> <h2>...</h2> (and others)
    text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    # new lines: \n -> <br>
    text = text.replace("\n", "<br>")

    return text


def parse_markdown_to_csv(input_md_path: str, output_csv_path: str, md_separator: str):
    r"""
    Converts a Markdown file with flashcard-style content into a CSV file compatible with Anki.

    The input '.md' file should contain questions starting with lines like '#Question', and a separator line
    (equal to `md_separator`) between the question and its corresponding answer.

    Each question and answer is parsed as a text block (multi-line supported), then converted to HTML
    using simplified Markdown parsing. This includes support for bold (`**...**`), italic (`*...*`),
    headers (`#`, `##`, `###`), and LaTeX expressions in `$...$` and `$$...$$`, which are replaced with
    `\\(...\\)` and `\\[...\\]` respectively for MathJax rendering.

    The output is a `.csv` file with two columns: the question and the answer. All newline characters
    are replaced with `<br>` tags to preserve formatting in Anki.


    Args:
        input_md_path (str): Path to the input Markdown file.
        output_csv_path (str): Path to the output CSV file.
        md_separator (str: Line separator that distinguishes questions from answers (e.g. '???').

    Returns:
        None. Writes a formatted '.csv' file ready for Anki import
    """
    with open(input_md_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_question: list[str] = []
    current_answer: list[str] = []
    notes: list[tuple[str, str]] = []
    mode = None

    def flush_note(q_lines: list[str], a_lines: list[str]) -> tuple[str, str]:
        q = "\n".join(q_lines).strip()
        a = "\n".join(a_lines).strip()
        return q, a

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# Question"):
            if current_question and current_answer:
                notes.append(flush_note(current_question, current_answer))
            current_question.clear()
            current_answer.clear()
            mode = "question"
        elif stripped == md_separator:
            mode = "answer"
        elif mode == "question":
            current_question.append(line.rstrip())
        elif mode == "answer":
            current_answer.append(line.rstrip())

    if current_question and current_answer:
        notes.append(flush_note(current_question, current_answer))

    with open(output_csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for question, answer in notes:
            writer.writerow([md_to_html(question), md_to_html(answer)])
