# About

This is SciPop, the friendly AI that analyses and synthesizes scientific articles for the general public.


```mermaid
flowchart TD
    Papers@{ shape: docs}
    DiVA@{ shape: database}
    RQE@{ shape: rect, label: "Research question
    extractor (GPT)"}
    RQL@{ shape: doc, label: "List of 
    research questions"}
    RQC@{ shape: rect, label: "Research question
    clusterer (BERTopic)"}
    RT@{ shape: doc, label: "Research topics"}
    CHS@{ shape: rect, label: "Challenge synthesizer (GPT)" }
    PS@{ shape: doc, label: "Problem - Solution
    statements"}
    RS@{ shape: rect, label: "Research synthesizer (GPT)"}
    Papers --> DiVA --> RQE --> RQL --> RQC --> RT --> CHS --> PS
    RT --> RS
    RS --> PS
    PS --Author review--> PS
```

# Environment setup

1. Install miniconda
2. Switch to the base environment

   `conda activate base`
3. Create a new conda environment and switch to it

   `conda create --name scipop python=3.12 pip`

    `conda activate scipop`
4. Install required packages

   `pip install -r requirements.txt`
