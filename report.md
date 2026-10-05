# Computational Astrophysics Homework 1 Report

**Author:** Tzu-Hsuan Lin  
**Date:** 2026-10-05  

---

## Problem 1 — Prompt-Structure Experiments

### Selected Question
Derive the orbital period of a circular orbit at altitude 550 km above Earth’s surface from Newtonian gravity, and evaluate it in minutes.

### Comparison Table

Ground truth: 95.50 minutes
LLM model: Gemini 3.5 Flash-Lite

+--------------+-------+------------------------------------------------------+------------------+-----------------------+--------------------------+---------------------------+
| Prompt Type  | Run # | Final Number Correct (Within 1% of the ground truth) | Derivation Steps | Units Consistent      | Output Format Followed   | Run-to-Run Consistency*   |
+--------------+-------+------------------------------------------------------+------------------+-----------------------+--------------------------+---------------------------+
| Unstructured | Run 1 | Yes (95.50 min)                                      | Yes              | Yes                   | N/A (Unconstrained)      | Medium                    |
| Unstructured | Run 2 | Yes (95.5  min)                                      | Yes              | Yes                   | N/A (Unconstrained)      | Medium                    |
| Unstructured | Run 3 | Yes (95.5  min)                                      | Yes              | Yes                   | N/A (Unconstrained)      | Medium                    |
+--------------+-------+------------------------------------------------------+------------------+-----------------------+--------------------------+---------------------------+
| Structured   | Run 1 | Yes (95.48 min)                                      | Yes              | Yes                   | Yes (Strict 4 sections)  | High                      |
| Structured   | Run 2 | Yes (95.48 min)                                      | Yes              | Yes                   | Yes (Strict 4 sections)  | High                      |
| Structured   | Run 3 | Yes (95.51 min)                                      | Yes              | Yes                   | Yes (Strict 4 sections)  | High                      |
+--------------+-------+------------------------------------------------------+------------------+-----------------------+--------------------------+---------------------------+
*Run-to-Run Consistency: The structured runs were more consistent in both response structure and numerical results, whereas the unstructured runs showed greater variation in formatting and additional content.

### Discussion of Prompting Performance

Comparing all six runs reveals distinct model behaviors associated with differences in prompt content.

1. Unstructured Runs
In the unstructured runs, the absence of explicit context guardrails allowed higher freedom. Even though the prompt did not specify the output format, all three runs automatically provided detailed derivations for orbital period and included Python code to calculate the final answer. However, because no structure was enforced, the formatting varied across runs. While all three runs correctly derived the period T(G, M, R_E, h) and carried units consistently, their responses provided additional information. Unstructured run1 and run3 included extra real-world example, referencing SpaceX's Starlink constellation. Furthermore, run2 and run3 appended secondary Python scripts to calculate the period using the WGS84 ellipsoidal Earth radius R_E = 6378.137 km. This shows that without clear boundaries in the prompt, the LLM might bring in extra information on its own.

2. Structured Runs
Structured prompting constrained the model's response and eliminated conversational flexibility. 
Providing fixed values of constants and parameters in <context> (G, M_earth, R_earth, h) eliminated parameter ambiguity. Unlike the unstructured runs, the structured runs did not introduce alternative Earth-radius values such as the WGS84 radius. Theoretical derivations across all three structured runs converged on identical physical steps, showing only minor algebraic formatting variations. Giving an explicit <output_format> made all three outputs follow the same format. In the numerical section, despite minor differences in expression, all runs showed the intermediate calculation steps in detail (r = R_earth+ h, T_sec, T_min). Minor differences in numerical evaluation resulted in small differences in the reported final values (95.48 to 95.51 minutes), yet all satisfied the 1% ground-truth tolerance from ground_truth.py (95.50 min). 

---

## Problem 2 — Hallucination hunt

---

## Problem 3 — Agent-assisted mini-tool with tests and clean git history

---

## Problem 4 — AI usage log
