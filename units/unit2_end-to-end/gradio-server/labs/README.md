# Gradio MCP Server — Lab (minimal scaffold)

This lab contains a tiny Gradio app used as a scaffold for the Unit 2 exercises.

Files

- `app.py` — minimal Gradio app that exposes a sentiment function (dependency-light heuristic).
- `requirements.txt` — Python dependencies (Gradio).

Run (PowerShell on Windows):

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open the local URL printed by Gradio to test the sentiment tool. Replace the heuristic in `app.py` with a real model or TextBlob/transformers pipeline for production labs.
# Unit 2 — Gradio MCP Server — Labs

- Lab: Build the minimal Gradio-based MCP server that exposes a sentiment tool.
- Add server code, requirements and run instructions in this folder.
