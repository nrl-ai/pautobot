<p align="center">
  <img alt="PAutoBot" style="width: 128px; max-width: 100%; height: auto;" src="./docs/pautobot.png"/>
  <h1 align="center">🔥 PⒶutoBot 🔥</h1>
  <p align="center" style="font-size:18px"><b>Private AutoGPT Robot</b> - Your private task assistant with GPT!</p>
</p>

**NOTE: This project is still in development.**

- **Ask questions** to your documents without an internet connection, using the power of LLMs. 100% private, no data leaves your execution environment at any point. You can ingest documents and ask questions without an internet connection! Engine developed based on [PrivateGPT](https://github.com/imartinez/privateGPT).
- **Automate tasks** easily with PAutoBot plugins. Easy for everyone!

Built with [LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Chroma](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [PrivateGPT](https://github.com/imartinez/privateGPT).

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

- Python 3.8 or higher.
- Install **PAutoBot**:

```shell
pip install pautobot
```

## 2. Usage

- Run the app:

```shell
python -m pautobot.app
```

- Go to <http://localhost:5678/> to see the user interface. You can choose one of the two modes:
  - **Chat**
  - **Chat + QA**
- Upload some documents to the app (see the supported extensions above).
- Ingest documents with **Ingest Data** button.
