#  Parallel Structural Reasoning System (Gemini API)

A modular multi-node reasoning system built using the Google Gemini API, designed to divide complex prompts into smaller logical sections, process them in parallel worker nodes, and combine results into a coherent answer.

This project demonstrates how to orchestrate structured reasoning across multiple LLM instances using Gemini — ideal for research, distributed LLM design, and structured text generation.

#  Features

🔹 Structural Decomposition: Splits a complex question into multiple reasoning sections.

🔹 Parallel Worker Nodes: Each section is processed independently by a worker LLM.

🔹 Composable Responses: Outputs from each worker can be merged into a single coherent answer.

🔹 Official Google GenAI SDK: Uses the official google-genai client for reliability and ease.

🔹 Extendable Design: Easily add aggregation or reasoning layers.

#  Project Architecture
main.py
│
├── GeminiClient          # Wrapper for Google Gemini API
│
├── StructuralClient      # Breaks a complex prompt into structured sub-sections
│
├── WorkerNodes           # Processes each section individually
│
└── structural_responsetojson()  # Converts structured plan into usable JSON

#  Flow Overview

Structural Planning
The StructuralClient sends the user’s query to Gemini and receives a structured JSON plan, dividing it into multiple sections.

Worker Node Execution
Each WorkerNodes instance receives one section’s title and instructions, generating detailed text output independently.

Aggregation (optional)
All worker node outputs can be merged to produce the final comprehensive answer.

#  Installation
1. Clone the Repository
git clone https://github.com/<your-username>/parallel-structural-reasoning.git
cd parallel-structural-reasoning

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # on macOS/Linux
venv\Scripts\activate       # on Windows

3. Install Dependencies
pip install google-genai python-dotenv

4. Add Your Gemini API Key

Create a .env file in the root directory:

GEMINI_API_KEY=your_google_gemini_api_key_here

#  Usage
Run the Main Script
python main.py


Example output:

[Section 1 Output]
Quantum computing is a new type of computation...

[Section 2 Output]
Superposition allows qubits to exist in multiple states...

# Example Breakdown

Input Prompt:

"Explain quantum computing in simple terms"

Structural Output (from StructuralClient):

{
  "num_workers": 4,
  "sections": [
    {"title": "What is Quantum Computing? (The Basics)", "instruction": "Provide a simple, high-level definition..."},
    {"title": "How Quantum Computers Work: Superposition and Entanglement", "instruction": "Explain superposition and entanglement..."},
    {"title": "What Can Quantum Computers Do? (Applications)", "instruction": "Describe potential applications..."},
    {"title": "Current Status and Future Outlook", "instruction": "Discuss current limitations and future potential."}
  ]
}


Each Section is Then Processed by a Worker Node:

Worker Node 1 → Explains the basics  
Worker Node 2 → Describes quantum principles  
Worker Node 3 → Lists applications  
Worker Node 4 → Discusses current challenges
