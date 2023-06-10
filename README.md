<p align="center">
  <img alt="PAutoBot" style="width: 128px; max-width: 100%; height: auto;" src="./docs/pautobot.png"/>
  <h1 align="center">🔥 PⒶutoBot 🔥</h1>
  <p align="center" style="font-size:18px"><b>Private AutoGPT Robot</b> - Your private task assistant with GPT!</p>
</p>

- 🔥 **Chat** to your offline **LLMs on CPU Only**. **100% private**, no data leaves your execution environment at any point.
- 🔥 **Ask questions** to your documents without an internet connection. Engine developed based on [PrivateGPT](https://github.com/imartinez/privateGPT).
- 🔥 **Automate tasks** easily with **PAutoBot plugins**. Easy for everyone.
- 🔥 **Easy coding structure** with **Next.js** and **Python**. Easy to understand and modify.
- 🔥 **Built with** [LangChain](https://github.com/hwchase17/langchain), [GPT4All](https://github.com/nomic-ai/gpt4all), [Chroma](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [PrivateGPT](https://github.com/imartinez/privateGPT).

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

## I. Installation and Usage

### 1. Installation

- Python 3.8 or higher.
- Install **PAutoBot**:

```shell
pip install pautobot
```

### 2. Usage

- Run the app:

```shell
python -m pautobot.app
```

or just:

```shell
pautobot
```

- Go to <http://localhost:5678/> to see the user interface. You can choose one of the two modes:
  - **Chat Only**
  - **Documents Q&A**
- Upload some documents to the app (see the supported extensions above). You can try [docs/python3.11.3_lite.zip](docs/python3.11.3_lite.zip) for a quick start. This zip file contains 45 files from the [Python 3.11.3 documentation](https://docs.python.org/3/download.html).
- Force ingesting documents with **Ingest Data** button.

You can also run PAutoBot publicly to your network or change the port with parameters. Example:

```shell
pautobot --host 0.0.0.0 --port 8080
```

## II. Development

### 1. Clone the source code

```shell
git clone https://github.com/nrl-ai/pautobot
cd pautobot
```

### 2. Run your backend

- Python 3.8 or higher.
- To install Pautobot from source, from `pautobot` source code directory, run:

```shell
pip install -e .
```

- Run the app:

```shell
python -m pautobot.app
```

- Go to <http://localhost:5678/> to see the user interface.

### 2. Run your frontend

- Install the dependencies:

```shell
cd frontend
npm install
```

- Run the app:

```shell
npm run dev
```

- Go to <http://localhost:3000/> to see the user interface. Use this address to develop the frontend.
