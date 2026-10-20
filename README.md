# Digital Signal Encoder, Scrambler & Decoder

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Assignment](https://img.shields.io/badge/Course-ITT%20036%20Data%20Communications-navy)](https://github.com/Roshae276/DATA_COMM_PROGRAMMING_ASSIGNMENT)
[![Report](https://img.shields.io/badge/PDF-Specification%20Report-red.svg)](specification_report.pdf)

> **ITT 036: Data Communications — Programming Assignment 1**  
> **Submission Deadline:** 21 October 2026  
> **Repository:** [https://github.com/Roshae276/DATA_COMM_PROGRAMMING_ASSIGNMENT](https://github.com/Roshae276/DATA_COMM_PROGRAMMING_ASSIGNMENT)

---

## 👥 Contributors

| Name | GitHub | Email |
| :--- | :--- | :--- |
| **Roshni Dodani** | [@Roshae276](https://github.com/Roshae276) | [roshae276@gmail.com](mailto:roshae276@gmail.com) |
| **Vansh Saini** | [@vanshsaini48](https://github.com/vanshsaini48) | [vansh.sainiwork@gmail.com](mailto:vansh.sainiwork@gmail.com) |
| **Prateek Kumar Singh** | [@prateekumarsingh9939-beep](https://github.com/prateekumarsingh9939-beep) | [prateekumarsingh9939@gmail.com](mailto:prateekumarsingh9939@gmail.com) |

---

## 📌 Project Overview

This project implements a complete, modular, and high-performance digital communication pipeline in Python 3.9+. It includes pseudo-random binary data generation, competitive-programming-grade palindrome search, line coding, bipolar scrambling, analog delta modulation, waveform visualization, and an **extra-credit image-parameter-based signal decoder**.

### 🌟 Key Features

1. **Digital Data Generator & Palindrome Search:**
   - Generates purely random binary streams.
   - Generates binary streams with deterministic blocks of $4$ or $8$ consecutive zeros for scrambling tests.
   - Computes the **longest palindromic substring** in optimal $\mathcal{O}(N)$ time using **Manacher's Algorithm** with sentinel transformation.

2. **Line Coding Schemes:**
   - **NRZ-L (Non-Return-to-Zero-Level):** Bit $0 \to +1\text{V}$, Bit $1 \to -1\text{V}$.
   - **NRZ-I (Non-Return-to-Zero-Invert):** Inversion on $1$, constant on $0$ (baseline: $-1\text{V}$).
   - **Manchester (IEEE 802.3):** Bit $0 \to [+1, -1]$, Bit $1 \to [-1, +1]$.
   - **Differential Manchester:** Boundary transition for $0$, no boundary transition for $1$; constant mid-bit transition for synchronization.
   - **AMI (Alternate Mark Inversion):** Bit $0 \to 0\text{V}$; Bit $1$ pulses alternate polarities between $+1\text{V}$ and $-1\text{V}$.

3. **Scrambling Techniques (AMI Add-on):**
   - **B8ZS (Bipolar with 8-Zero Substitution):** Replaces $0^8$ with $[0, 0, 0, p, -p, 0, -p, p]$ where $p$ matches the preceding pulse polarity.
   - **HDB3 (High-Density Bipolar 3-Zero):** Replaces $0^4$ with $000V$ (odd pulse count since last substitution) or $B00V$ (even pulse count) to guarantee zero DC drift.
   - Includes full forward unscramblers recovering the original bitstream.

4. **Analog Delta Modulation (DM):**
   - Implements a Delta Modulation encoder tracking analog samples with an adjustable step size $\Delta$.
   - Reconstructs continuous analog signals through a staircase decoder.

5. **🏆 Extra Credit: Image-Based Signal Decoder:**
   - Decodes encoded signals directly by analyzing the physical parameters (RGB pixel columns, baseline center, and vertical deflection) of exported PNG waveform images at 100 DPI.
   - Does **not** inspect internal data arrays or variables during image decoding, strictly adhering to the assignment's extra-credit mandate.

6. **Graphical Visualization:**
   - Plots discrete step waveforms via Matplotlib.
   - Provides side-by-side dual-panel comparative plots of un-scrambled AMI vs. scrambled (B8ZS/HDB3) signals.

---

## 📂 Repository Structure

```text
DATA_COMM_PROGRAMMING_ASSIGNMENT/
├── data_generator.py       # Random sequence generator & Manacher's Algorithm
├── line_coding.py          # Line coding encoders (NRZ-L, NRZ-I, Manchester, AMI)
├── decoder.py              # Direct line coding decoders
├── scrambling.py           # B8ZS & HDB3 scrambling and unscrambling algorithms
├── modulation.py           # Delta Modulation (DM) encoder & staircase decoder
├── signal_plotter.py       # Matplotlib waveform plotting and comparison figures
├── image_decoder.py        # Extra credit: Image-parameter waveform decoder
├── main.py                 # Interactive CLI orchestrating complete user workflow
├── specification_report.tex# 1-page LaTeX specification report source
├── specification_report.pdf# Compiled official 1-page PDF specification report
├── requirements.txt        # Project dependencies (NumPy, Matplotlib, Pillow)
└── test_images/            # Sample exported waveform images for testing
```

---

## ⚡ Algorithmic Complexity

In accordance with competitive-coding criteria, all algorithms avoid recursion, nested iteration, and exhaustive branching:

| Component | Time Complexity | Space Complexity | Algorithm / Design Principle |
| :--- | :---: | :---: | :--- |
| **Palindrome Search** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Manacher's Algorithm with `#` sentinels |
| **Line Encoders & Decoders** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Single-pass linear symbol mapping |
| **B8ZS / HDB3 Scramblers** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Lookahead window pattern substitution |
| **B8ZS / HDB3 Decoders** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Single-pass violation pattern detector |
| **Delta Modulation** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Single-pass sample step accumulator |
| **Image Waveform Decoder** | $\mathcal{O}(W \times H)$ | $\mathcal{O}(W \times H)$ | 2D pixel array column threshold scan |

*$N$ = number of bits or samples; $W, H$ = width and height of the waveform image.*

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9 or higher (standard CPython; no MATLAB or Octave required).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Roshae276/DATA_COMM_PROGRAMMING_ASSIGNMENT.git
   cd DATA_COMM_PROGRAMMING_ASSIGNMENT
   ```

2. **Create and activate a virtual environment:**
   * **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * **Windows:**
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 How to Run

### Interactive Application
Launch the main CLI runner:
```bash
python main.py
```

**Workflow Walkthrough:**
* Select **`1`** for **Digital Input**:
  1. Choose between manual input, purely random data, or data seeded with $4$ or $8$ consecutive zeros.
  2. The longest palindromic substring is computed and printed via Manacher's Algorithm.
  3. Select an encoding scheme: `NRZ-L`, `NRZ-I`, `Manchester`, `Differential Manchester`, or `AMI`.
  4. If `AMI` is selected, prompt will query whether scrambling (`B8ZS` or `HDB3`) is desired.
  5. Waveform plots are rendered and saved as PNG files.
  6. Choose whether to decode the signal back to raw bits (direct decoder or image-based decoder).
* Select **`2`** for **Analog Input (Delta Modulation)**:
  1. Provide analog sample values, quantization step size $\Delta$, and initial reference.
  2. Generates the DM bitstream and reconstructs the staircase output signal.

### Standalone Image Decoder Verification (Extra Credit)
To test image-parameter waveform decoding on sample PNG waveforms:
```bash
python image_decoder.py
```

---

## 📄 Specification Report

An official **1-page Specification Report** has been typeset in LaTeX and compiled to PDF:
* **PDF File:** [`specification_report.pdf`](specification_report.pdf)
* **LaTeX Source:** [`specification_report.tex`](specification_report.tex)

The document is formatted to fit strictly onto one single page as required by assignment guidelines.

---

## 📚 References & Sources

1. **B. A. Forouzan**, *Data Communications and Networking*, 5th ed., McGraw-Hill, 2013 (Chapter 4: Digital Transmission; Chapter 5: Analog Transmission).
2. **W. Stallings**, *Data and Computer Communications*, 10th ed., Pearson, 2013.
3. **G. Manacher**, "A new linear-time algorithm for finding the smallest initial palindrome of a string," *Journal of the ACM*, vol. 22, no. 3, pp. 346–351, 1975.
4. [GeeksforGeeks: Manacher's Algorithm](https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/)
5. [Wikipedia: Bipolar Encoding & Scrambling (B8ZS / HDB3)](https://en.wikipedia.org/wiki/Bipolar_encoding)
6. [Wikipedia: Delta Modulation Principles](https://en.wikipedia.org/wiki/Delta_modulation)
7. [Python Standard Library `random` Module](https://docs.python.org/3/library/random.html)
8. [NumPy Documentation](https://numpy.org/doc/stable/) · [Matplotlib Documentation](https://matplotlib.org/stable/) · [Pillow Documentation](https://pillow.readthedocs.io/)

---

## ⚖️ Academic Integrity & AI Tools Declaration

In compliance with the assignment policy:
* The team acknowledges the exploratory use of AI tools for initial boilerplate scaffolding.
* All generated code was thoroughly reviewed, debugged (including resolving edge-case B8ZS polarity reversal bugs), optimized to $\mathcal{O}(N)$ using Manacher's Algorithm, and manually integrated by team members.
* Plagiarism guidelines and academic integrity standards have been strictly observed.
