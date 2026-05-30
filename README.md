# hybrid-md-mpcd-vicsek

## Project Overview
This repository contains a high-performance computational study of active matter dynamics, specifically focusing on the emergence of collective motion and the role of hydrodynamic interactions in clustering. The project replicates and extends the foundational Vicsek Model (1995) by integrating it into a modern explicit solvent framework using the hybrid MD-MPCD methodology described in the 2022 Bera et al. research paper.

The simulation demonstrates how simple local alignment rules lead to spontaneous symmetry breaking and how the presence of a fluid medium transforms cluster growth from "diffusive coalescence" into high-velocity ballistic aggregation.

---

## Key Scientific Features
* **Vicsek Alignment Principle:** Implements the rule where self-driven particles assume the average direction of their neighbors, triggering a kinetic phase transition from disorder to ordered transport.
* **Explicit Solvent Hydrodynamics:** Utilizes Multiparticle Collision Dynamics (MPCD) to simulate a high-density solvent ($10/\sigma^3$) that conserves mass, momentum, and energy, effectively modeling the "swimmer flows" that drive aggregation.
* **Clustering Dynamics:** Captures the shift in growth laws where average cluster mass evolves as $M \sim t$. It specifically validates the ballistic aggregation (BA) mechanism, where activity and hydrodynamics lead to significantly faster growth compared to passive systems.
* **Force Modeling:** Employs Force-Shifted Lennard-Jones for Passive Attractive (PA) interactions and WCA potentials for repulsive active-solvent interactions, ensuring physical "overlap-avoiding" behavior.

---

## Technical Implementation
* **Simulation Engine:** Built on HOOMD-blue v5.0.1, leveraging its robust Molecular Dynamics (MD) and MPCD integration capabilities.
* **Performance & Scaling:** Optimized for GPU acceleration (tested on NVIDIA 1050 GTX), enabling the simulation of ~13,000 particles across 15,000 timesteps in a complex 3D periodic box ($L=64\sigma$) within 3-4 hours.
* **Environment Management:** Developed within a virtual Linux kernel (WSL) using Pixi for a reproducible, isolated scientific computing ecosystem.
* **Integration Scheme:** Uses the Velocity Verlet algorithm for precise particle trajectory updates alongside stochastic rotation dynamics for the solvent.

---

## Analysis & Validation Tools
The repository includes custom Python-based analysis scripts for:
* **Mean-Squared Displacement (MSD):** Confirming the quadratic enhancement of cluster motion characteristic of ballistic aggregation.
* **Velocity Correlation (Cvv):** Measuring the alignment of velocity directions within clusters to quantify the strength of hydrodynamic influence.
* **Cluster Analysis:** Functions to identify disconnected clusters and calculate their mass distributions ($M$) as the first moment of the distribution function.

---

## Scientific References
* **Vicsek et al. (1995):** *Novel Type of Phase Transition in a System of Self-Driven Particles.*
* **Bera et al. (2022):** *Active particles in explicit solvent: Dynamics of clustering for alignment interaction.*
