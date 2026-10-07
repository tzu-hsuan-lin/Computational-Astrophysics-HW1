# HW1 - Computational Astrophysics

Deliverables for HW1: Prompting, Hallucinations, and an Agent-Built Mini-Tool (Fall 2026, NTHU).

## Prerequisites & Environment Setup

This repository uses **Python 3.11+** and `uv` for environment and dependency management.

To set up the pinned environment:
```bash
uv sync

## Running & Verifying Deliverables

### Problem 1: Prompt-Structure Experiments

Ground Truth Script: The orbital period of a circular orbit at altitude 550 km above Earth’s surface
	uv run python ground_truth.py
Transcripts: Unstructured prompt, structured prompt, and the responses from the LLM.
	Stored in /transcripts/p1/

### Problem 2: Hallucination Hunt

Unit Conversion: erg s^-1 cm^-2 Hz^-1 --> Jy --> AB magnitude --> # photons cm^-2 s^-1 keV^-1

Transcripts: Failed response form LLM with hallucination and response with mitigation. 
	Stored in /transcripts/p2/
Verification: Unit conversion computation
	uv run python P2_unit_conversion.py

### Problem 3: Agent-Assisted Kepler Solver

Run Acceptance Test Suite:
Executes all 8 unit tests in tests/test_kepler.py covering scalar/vectorized inputs, symmetry, e=0 identity, M outside [0, 2pi), and residual tolerances |E - e sin(E) - M| < 10^-10 across 1000 random (M, e) pairs with e in [0, 0.99]

Run the tests in /tests/:
	uv run pytest

### Problem 4: AI Usage Log
AI_LOG.md at the repository root contains the information of which AI tools and how AI helped me with this homework.

### Report
Report of this homework is written in report.md at the repository root.


