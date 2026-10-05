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

## Problem 2 — Hallucination hunt (Astrophysical Unit Conversion)

LLM Model: GPT-5.6 Luna

### 1. The Failure Mode

In the baseline prompt, GPT-5.6 Luna was asked to convert the flux density F = 3.5 × 10⁻¹³ erg s⁻¹ cm⁻² Hz⁻¹ at 1 keV into Jansky, AB magnitude, then photon flux (N_E) in photon cm⁻² s⁻¹ keV⁻¹. 
While the model correctly calculated the flux density in Jansky (3.5 × 10¹⁰ Jy) and AB magnitude (-17.46), it exhibited a unit conversion hallucination when evaluating the photon flux. The model showed N_E = 3.5 × 10⁻¹³ / (6.626 × 10⁻²⁷ × 1.602 × 10⁻⁹) ≈ 3.30 × 10²² photons cm⁻² s⁻¹ keV⁻¹.
It incorrectly converted the unit of the photon energy from keV to erg by inserting an additional keV-to-erg conversion factor (1.602 × 10⁻⁹ erg/keV) in the denominator, leading to a wrong result.

### 2. Verification

A Python script (P2_unit_conversion.py) was written to verify all conversions of units step by step, following a sequential calculation: Flux Density (F_nu) -> Jansky (F_Jy) -> AB Magnitude (m_AB) -> Photon Flux Density (N_E).

1. Flux Density to Jansky:
    F_nu = 3.5 × 10⁻¹³ erg s⁻¹ cm⁻² Hz⁻¹
    1 Jy = 10⁻²³ erg s⁻¹ cm⁻² Hz⁻¹ 
    F_Jy = F_nu × 10²³ = 3.50 × 10¹⁰ Jy 

2. Jansky to AB Magnitude:
    m_AB = -2.5 × log10(F_Jy / 3631 Jy) ≈ -17.46 

3. AB Magnitude to Photon Flux (N_E): 
    Convert m_AB back to CGS flux density (F_CGS): 
	F_AB_to_Jy = 3631 × 10^(-0.4m_AB) Jy 
	F_CGS = F_AB_to_Jy / 10²³ erg s⁻¹ cm⁻² Hz⁻¹ 
    Bandwidth & Energy Conversion: 
	1 keV = 1.602 × 10⁻⁹ erg 
	Photon energy is h × nu = E_keV × (1.602 × 10⁻⁹ erg/keV) 
	Differentiating gives d_nu / dE_keV = (1.602 × 10⁻⁹) / h 
	Energy flux per keV: F_E = F_CGS × (1.602 × 10⁻⁹) / h (erg s⁻¹ cm⁻² keV⁻¹) 
    Photon Count Conversion: 
	N_E = F_E / (Energy per photon) = F_CGS / (h × E_keV) ≈ 5.28 × 10¹³ photons cm⁻² s⁻¹ keV⁻¹ 

The execution of P2_unit_conversion.py confirmed these outputs:
* Flux density = 3.50e+10 Jy
* AB magnitude = -17.46
* Photon flux = 5.28e+13 photon cm^-2 s^-1 keV^-1

### 3. Mitigation Results

A new prompt asked a fresh conversation of the LLM model to restate all constants, double-check the unit conversion, and say "I don't know" if it was not sure. With these rules, the model made a correct calculation and got the correct answer of 5.28 × 10¹³ photons cm⁻² s⁻¹ keV⁻¹.

### 4. Why This Failure Happens

This failure happens because LLMs generate text step-by-step without an internal calculator. In the baseline prompt, the model tried to output the final answer directly, essentially guessing some words based on what it had memorized or seen during training without checking if the units actually matched.

By requiring the model to show intermediate steps and check units, the prompt forced it to break down the formula. Writing out the full equation and units step-by-step provided the critical context needed for the LLMs to predict the next token. This demonstrates that prompting for explicit reasoning helps the model use its own intermediate steps to avoid errors and reach physically accurate conversions.

---

## Problem 3 — Agent-assisted mini-tool with tests and clean git history

---

## Problem 4 — AI usage log
