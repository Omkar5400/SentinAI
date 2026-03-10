SentinAI: RAG-Powered Android Compliance Auditor
An intelligent security agent that audits Android applications against the official Android 14 Compatibility Definition Document (CDD) using Retrieval-Augmented Generation (RAG).

🚀 Architecture
Mobile (The Body): Android (Kotlin) application that performs real-time scanning of installed packages, metadata, and requested permissions.

Backend (The Brain): FastAPI (Python) server utilizing Llama 3.2 for reasoning and audit generation.

Vector Database: FAISS with HuggingFace embeddings (all-MiniLM-L6-v2) for high-speed retrieval of compliance rules from a local knowledge base.

🧠 Core Workflow
Extraction: The Android client identifies sensitive permission strings from the device's package manager.

Retrieval: The Python backend queries the vector store to pull specific compliance sections from the Android 14 CDD.

Reasoning: The LLM analyzes the app's permissions against the retrieved CDD context to generate a factual risk score (1-10) and verdict.

Delivery: The mobile UI dynamically color-codes results (Safe/Warning/Critical) based on the AI's structured response.

🛠️ Key Optimizations
Grounded Audits: Leverages RAG to eliminate AI hallucinations by forcing the model to cite official compliance documentation.

Privacy-First Design: Optimized for Apple Silicon (M-series); all inference runs locally via Ollama. No sensitive app metadata ever leaves the local environment.

Asynchronous Stability: Implemented a 1-second throttled communication layer between Android Coroutines and the FastAPI engine to ensure UI responsiveness during heavy AI processing.

Quick Start
Start the Brain:

Bash
ollama run llama3.2
cd SentinAI_Backend
python3 Main.py

Launch the Body:
1) Open SentinAI_Mobile in Android Studio.
2) Run on an emulator (Targeting API 34+).
3) Ensure the server URL is pointed to 10.0.2.2:8000.
