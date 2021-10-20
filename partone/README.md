# Part 1: ML/Data Orchestrators, Flyte Overview

This part will introduce you to ML/data orchestration and take you through a deeper dive into Flyte. We will start with what an ML/data pipeline orchestration tool is and the desired use cases. We will follow this discussion with the considerations, trade-offs, and motivation that led to the design of Flyte, an introduction to Flyte, its features, and components. Later, we will talk about how Flyte is different from other orchestration tools and showcase how Flyte scales at various organizations. We will end this part by giving you a glimpse into the Flyte open source community and the roadmap.

- ML pipeline, from procuring data to serving the model
- ML and Data pipeline orchestration tools: need of the hour!
- Desired use cases
  - Serverless experience
  - Consistent APIs for jobs and pipelines
  - Parameterize executions
  - Dynamic workflows
  - Development and iteration
  - Ops and visibility
  - Reusability and shareability
  - Extensibility and flexibility
- About Flyte
  - What is Flyte?
  - Features
    - Kubernetes-native
    - Ergonomic SDKs in Python, Java & Scala (Flytekit)
    - Multi-tenancy
    - Data lineage and memoization
    - Dynamism
    - Reproducibility
    - Strongly typed system
    - Versioned and auditable
  - Components
    - FlyteAdmin
    - FlytePropeller
    - Flyte Console
    - FlyteCTL
    - Overall architecture
  - Flyte user journey
  - Flyte vs. others
- Case studies: witness Flyte’s scalability
  - Lyft
  - Spotify
  - Freenome
- Flyte open-source community
- Roadmap
