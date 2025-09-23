# About

This is SciPop, the friendly AI that analyses and synthesizes scientific articles for the general public.


```mermaid
flowchart LR
    Papers@{ shape: docs, label: "DIPT\npublications"}
    DiVA@{ shape: database, label: "DiVA: Titles,\nabstracts and meta-data"}
    RAC@{ shape: rect, label: "Research abstract\nclusterer (BERTopic)"}
    RT@{ shape: docs, label: "Research\nthemes"}
    RTP@{ shape: rect, label: "Research-to-practice\nsynthesizer (GPT)" }
    RTS@{ shape: docs, label: "Research themes\nsyntheses" }
    Papers --> DiVA --> RAC --> RT --> RTP --> RTS
    RTS --Research theme
 editor review--> RTS
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
