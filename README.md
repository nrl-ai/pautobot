<p align="center">
  <img alt="PAutoBot" style="width: 128px; max-width: 100%; height: auto;" src="./docs/pautobot.png"/>
  <h1 align="center">🔥 PⒶutoBot 🔥</h1>
  <p align="center" style="font-size:18px">Private AutoGPT Robot - Your private task assistant with GPT!</p>
</p>

**NOTE: This project is still in development.**

- **Ask questions** to your documents without an internet connection, using the power of LLMs. 100% private, no data leaves your execution environment at any point. You can ingest documents and ask questions without an internet connection! Engine developed based on [PrivateGPT](https://github.com/imartinez/privateGPT).
- **Automate tasks** easily with PAutoBot plugins. Easy for everyone!

![PAutoBot](./docs/screenshot.png)

**The supported extensions are:**

- `.csv`: CSV,
- `.docx`: Word Document,
- `.doc`: Word Document,
- `.enex`: EverNote,
- `.eml`: Email,
- `.epub`: EPub,
- `.html`: HTML File,
- `.md`: Markdown,
- `.msg`: Outlook Message,
- `.odt`: Open Document Text,
- `.pdf`: Portable Document Format (PDF),
- `.pptx` : PowerPoint Document,
- `.ppt` : PowerPoint Document,
- `.txt`: Text file (UTF-8),

# I. Installation and Usage

## 1. Installation

- Python 3.10 or higher.
- Install **PAutoBot**:

```shell
pip install pautobot
```

## 2. Usage

- Put your documents in `pautobot-data/documents` folder.
- Ingest documents:

```shell
python -m pautobot.ingest
```

- Run the app:

```shell
python -m pautobot.app
```

Go to <http://localhost:5678/> to see the app.
