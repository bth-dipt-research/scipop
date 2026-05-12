---
title: Research Group Synthesis
slug: research-group
summary: A top-level synthesis summarizing major themes across the research group portfolio.
reviewed_at: 2026-05-06
cluster_id: research-group
status: approved
editor_name: Prof. Tony Gorschek
editor_email: tony.gorschek@bth.se
editor_photo: /images/tony-gorschek.jpg
---
## Introduction

Software engineering is the core engineering discipline behind almost every
product and service in modern industry. Cars, telecom networks, medical devices,
manufacturing platforms, energy systems, public services, financial systems,
marine systems, games and entertainment are all software-intensive products and
services (SIPS) — products and services in which software is not a component but
the medium through which value is created, delivered, and evolved. The Software
Engineering Research Lab (SERL) at Blekinge Institute of Technology studies how
SIPS are conceived, designed, built, validated, deployed, and maintained over
their lifespan. Our work is empirical, applied, and built around long-term
collaboration with industry partners across telecom, automotive, defence,
fintech, manufacturing, entertainment and many other sectors.

The research portfolio is currently shaped by two transformations that affect
the entire discipline: the use of generative AI as an instrument of engineering
work (AI for Software Engineering, AI4SE), and the engineering of products and
services that contain AI components (Software Engineering for AI, SE4AI). Around
these two directions, we maintain long-running research lines on continuous
delivery, requirements and testing, security and operations, and how software is
developed at scale.

## AI for Software Engineering (AI4SE)

AI4SE concerns how the practices and principles of software engineering shift
when engineers use generative AI as an instrument of their work — to write code,
generate tests, refine requirements, explore design alternatives, document
systems, support reviews, and analyse defects. Each use is plausible; each
carries risks the discipline does not yet fully understand. We study these uses
empirically, in real industrial settings, with the aim of distinguishing genuine
improvement from acceleration of existing practice and from new failure modes
that traditional quality assurance does not catch.

## Software Engineering for AI-based systems (SE4AI)

SE4AI concerns how the engineering of products and services adapts when the
systems being built contain AI components. AI components are non-deterministic,
depend on data distributions that drift, can fail in ways that traditional
testing does not catch, and raise unfamiliar questions about safety, security,
traceability, regulatory compliance, and maintenance over time. The systems
containing them are no longer fully specifiable in advance, no longer fully
testable through coverage-based methods, and no longer fully predictable in
long-term behavior. SE4AI is not the engineering of AI itself; it is the
engineering of products and services in which AI sits as one component among
many.

Both AI4SE and SE4AI permeate all the engineering areas we work with - below an
overview of current research areas within Software Engineering.

## Continuous Delivery, Reuse, and Quality

Our research on continuous software engineering takes a cost-benefit perspective
on continuous integration and continuous delivery: which benefits are actually
attainable in industrial practice, what investments and risks they require, and
which contextual parameters determine whether the investment pays off. We study
strategic reuse as an organizational capability rather than a library of
components — how InnerSource practices, microservice ecosystems, CI/CD
pipelines, and decision models for component selection sustain reuse at
industrial scale. Our quality research connects internal-quality measures to
maintainability, reliability, and long-term evolution cost, including the role
of code review and how review knowledge propagates across teams. We also work
significantly with efficiency and effectiveness as quality aspects, and
value-driven engineering: how well and efficiently does a SIPS solve a problem
for the user or user’s organization?

## Requirements, Testing, and Traceability

Our requirements engineering research develops the empirical foundations for
what makes requirements fit for purpose, building toward measurement frameworks
that connect requirements quality to its impact on subsequent development
activities. Substantial work addresses regulatory compliance as a
requirements-level concern. Compliance automation, impact on generative
components and compliance, the cost and impact of compliance, automated
verification and validation in relation to compliance, and automated extraction
of compliance requirements from regulatory artifacts are but a few directions.

Our verification and validation research (e.g. testing) focuses on the
long-running challenge of GUI test automation: similarity-based and
LLM-supported web element localization, augmented testing for manual GUI
regression, code-review guidelines, and on traceability — including taxonomic
trace links and a systematic mapping of auxiliary artefacts in requirements
traceability. Significant resources are going into new methods, models,
principles and practices for quality assurance of (Gen)AI-intensive SIPS, that
is how do we quality assure generative components as part of a system without
limiting the capacity and flexibility it offers.

## Security, Privacy, and Operations

Our work treats security and privacy as routine engineering activities rather
than separate disciplines applied late. Software security maturity is
investigated empirically in industrial settings — for example, evaluating the
OWASP Software Assurance Maturity Model. Threat modelling for AI-intensive
systems is a growing focus where we for example have developed a Machine
Learning Security Maturity Model and recent work on threat modelling for
LLM-integrated applications. Privacy is studied as an engineering activity
rather than a compliance afterthought, including work on Privacy by Design and
GDPR alignment with software specifications. For operations, we study how
engineering organisations build and maintain confidence in CI/CD pipelines,
including non-functional testing in CI environments and the asset structure that
supports development and operations of software-intensive products and services.

## Ways of Working at Scale

Our research on hybrid and post-pandemic work characterises how performance,
productivity, and team functioning evolve when on-site presence is partial — the
conditions under which hybrid arrangements actually work, and the practices that
sustain coordination when they do not. We have studied psychological safety in
remote settings, and the conditions that draw engineers back to physical
workplaces). At organisational scale, we study decentralised decision-making,
communities of practice, ownership and clone governance in shared codebases, and
the alignment between technical architecture and organisational structure —
including recent work on the dynamics of cross-organisational software
collaboration. The shared theme across this work is making organisational and
architectural choices visible, measurable, and revisable. We also have a
long-tradition of lean/agile work research and value-based engineering
practices, where value measurement and outcomes are evidence-driven.

## Current research directions - and immediate future

Two focuses currently shape our research agenda. First, AI4SE: where we look at
how AI affects the principles of Software Engineering. Second, SE4AI, where we
look at how the engineering of products and services adapt whit AI build-in. All
process areas (traditional SWEBOK), from requirements, design, architecture,
coding, verification and validation, evolution, maintenance, and more need to be
rethought! If we take coding/development as an example. We will use GenAI to
improve, automate, support and speed-up coding (AI4SE) – but what are the
implications of this this? GenAI introduces new types of errors, new types of
limitations born from challenges with context windows, where do we draw the line
between human and machine work and responsibility, what can humans do when they
are not writing all code that adds value beyond what we do today. Looking at the
other perspective. If GenAI augments a human developer to code, what type of
architectures do we need going forward that takes advantage of the capacity, but
takes GenAI limitations into consideration, and how do we handle non-functional
(quality aspects) such as usability and security. All of this and much more
promises a bright future for Software Engineering and Software Engineering
research!

## A special note: How we work with partners

We do not work like traditional academic researchers. Our research does not
start at a desk, get tested on toy examples, and finish in a publication that no
industry partner has any way to use. It starts with real industrial problems,
develops candidate solutions in cooperation with the people who will use them,
and validates those solutions step by step in the settings where they have to
work. The figure below shows the cycle of co-production developed as early as
2006 but has evolved over the years (Gorschek, Garre, Larsson and Wohlin (IEEE
Software, 2006).

![co-production cycle](/images/coproduction.jpg)

Each research project moves through these seven steps. It begins on the industry
side, with a real problem (1) identified through on-site presence and
observation — not a topic chosen because it suits the literature. The research
agenda crosses into academia, where the question is formulated rigorously and
the relevant state of the art is studied (2), normally in cooperation with
industrial champions who help us understand the domain. We also separate the
symptoms from the actual problem (root cause). A candidate solution (3) is then
designed jointly with industry — drawing on existing research where possible,
and adding new contributions where needed. The solution is first validated in
academia (4) through controlled experiments and lab studies; this catches
obvious flaws cheaply, before any industrial resources are committed. It then
returns to the industry side for static validation (5) — widespread presentation
to practitioners and management through seminars and interviews, gathering
feedback and shaping the solution further. Dynamic validation (6) follows:
piloting in a real industrial project, with real engineers, on real artefacts,
but with limited scope so risk stays manageable. Only after the solution
survives all this is it released (7), with the tailoring, training, and tool
support that make adoption possible. The key is that we as researchers have to
measure the benefit of a “solution” in an objective way. This is needed for
publications and research, but is a huge benefit for partners as it gives
transparent evidence before investment into the new solution. We do not sell
solutions – we prove them. This is the SERL way.
