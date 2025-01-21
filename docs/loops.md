# Loops

The following two sequence diagrams visualize the two loops that populate the competence map with content.
The competence map is goverened by two loops.

## Loop 1: Topic Clustering

The first sequence diagram describes the big loop (executed twice a year) that generates our current research clusters from publications and applications.

```mermaid
sequenceDiagram

participant cmap as main
participant diva as DiVA
actor pi as PI
participant rqex as ExtractorGPT
participant clust as ClusterGPT

cmap ->>+ diva : getPublications(DIPT, last 10 years)
diva -->>- cmap : [publication]

cmap ->>+ pi : getApplications()
pi -->> cmap : [application]

cmap ->>+ rqex : extractRQs([publication])
rqex -->>- cmap : [RQ]

cmap ->>+ clust : cluster([RQs], [application])
clust -->>- cmap : [cluster]

cmap ->> pi : vet([cluster])
pi -->>- cmap : confirm
```

## Loop 2: Gathering Evidence

The second sequence diagram describes the small loop (executed once per month) that populates these clusters with recent evidence. 

```mermaid
sequenceDiagram

participant cmap as main
participant diva as DiVA
participant class as ClassifierGPT

cmap ->>+ diva : getPublications(DIPT, last month)
diva -->>- cmap : [publication]

cmap ->>+ class : classify([publications])
class -->>+ cmap : [cluster]

cmap ->> cmap : addEvidence([publication], [cluster])
```
