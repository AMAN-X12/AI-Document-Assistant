AI Document Assistant

This project was built to deeply understand RAG internals instead of relying only on high-level frameworks.

Overview

A production-ready Retrieval-Augmented Generation (RAG) system that enables contextual question answering over uploaded documents.

The project includes two retrieval architectures:

FAISS-based vector search (local embedding pipeline)

API-based embeddings with a custom cosine similarity engine

Architecture Variants
Version 1 — Local Embeddings + FAISS

Stack:

SentenceTransformers (local embeddings)

FAISS (vector indexing)

FastAPI backend

Flow:
Document → Chunking → Local Embeddings → FAISS Index
User Query → Embed → FAISS Search → Top-K → LLM → Answer

Version 2 — API Embeddings + Custom Retrieval Engine

Stack:

Embedding API

Manual cosine similarity (dot product implementation)

In-memory vector storage

Conversation memory integration

Flow:
Document → Chunking → API Embeddings → Store Vectors
User Query → Embed → Cosine Similarity (Dot Product) → Top-K → Add Chat Memory → LLM → Answer

Why This Is Powerful

This project demonstrates:

Deep understanding of RAG architecture

Practical knowledge of vector mathematics (cosine similarity)

Ability to build both framework-based and custom retrieval systems

Production API deployment

Memory-aware conversational system design
