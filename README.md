# Slowpitch Performance Lab

## Screenshots

### Upload
![Upload](assets/screenshot-upload.png)

### Results
![Results](assets/screenshot-results.png)

### Performance Chart & Team Analaysis
![Analysis](assets/screenshot-analysis.png)

### Player Comparison
![Comparison](assets/screenshot-comparison.png)

---

## What This Solves

Helps softball teams answer:

- Who should bat where?
- How much does lineup order matter?
- Which players actually drive runs?
- What lineup scores the most runs?


---

A full-stack softball analytics platform that transforms GameChanger CSV exports into actionable lineup decisions, player evaluations, and run projections.

---

## Live Demo

https://slowpitchlab.mattmartiny.com

---

## Features

- Upload GameChanger CSV exports  
- Player performance scoring (Offensive Value, Value per PA)  
- Archetype classification (Power, High Floor, Boom/Bust, etc.)  
- Optimized 12-player batting order generation  
- Interactive lineup editor (reorder players)  
- Run projection simulator (Monte Carlo simulation)  
- Lineup comparison (optimized vs user-adjusted)  
- Player comparison tool  
- Visual analytics (performance scatter plot)  

---

## Overview

This project combines data engineering, analytics, and simulation modeling to replicate real-world baseball decision-making workflows.

## Offensive Value Formula

The core metric used to evaluate hitters is **Offensive Value (OV)**, a weighted scoring model designed specifically for slowpitch softball.

    offensive_value = (
        1B * 1.1
        + 2B * 1.8
        + 3B * 2.4
        + HR * 3.0
        + BB * 0.95
        + ROE * 1.0
        + R * 0.25
        + RBI * 0.25
        - OUT * 0.5
    )

### Key Principles

- **Extra base hits are highly valuable**  
  Doubles, triples, and home runs drive the majority of run production.

- **Walks are strongly valued**  
  Reflecting slowpitch strategy where getting on base is critical.

- **Runs and RBIs are included as context**  
  Light weighting rewards players who consistently contribute to scoring without overpowering the model.

- **Outs are penalized**  
  Inefficient plate appearances reduce overall value.

---

## 📊 Efficiency Metric

    Value per PA = Offensive Value / Plate Appearances

This allows fair comparison across players with different playing time.

---

### Notes

- Inspired by wOBA, but tuned for slowpitch softball environments  
- Designed to balance player skill (hitting) with production (runs created)  
- Weights can be adjusted to better fit specific leagues or play styles  


## Model Limitations

While the Offensive Value model and simulation engine provide strong directional insights, there are important limitations to consider:

### Context Dependence (Runs & RBIs)
- Runs and RBIs depend heavily on lineup position and teammates  
- A player batting in the middle of the order will naturally accumulate more RBIs  
- These stats are included with light weighting to avoid overvaluing context

---

### Simplified Base Running Model
- The simulation uses simplified advancement rules (e.g., singles and walks advance runners predictably)  
- Does not account for:
  - Aggressive base running  
  - Player speed  
  - Situational decisions  

---

### No Situational Hitting
- All plate appearances are treated equally  
- Does not model:
  - Clutch hitting  
  - Two-out performance  
  - Situational approaches  

---

### Static Player Probabilities
- Player outcomes are based on historical averages  
- Does not adjust for:
  - Hot/cold streaks  
  - Pitcher quality  
  - Game conditions  

---

### League-Specific Tuning
- The weighting system is tuned for slowpitch softball environments  
- May not generalize perfectly to:
  - Other leagues  
  - Different skill levels  
  - Different field sizes or rules  

---

### No Defensive Impact
- The model focuses entirely on offensive production  
- Defensive value is not included  

---

## Interpretation Guidance

This tool is best used to:

- Compare players within the same team  
- Evaluate lineup structure and balance  
- Estimate relative run production differences between lineups  

It should not be treated as a precise predictor of game outcomes, but rather as a decision-support tool for lineup optimization.


### Data Pipeline
- Cleans and normalizes multi-header GameChanger exports  
- Handles missing data (e.g., derives singles from hits)  
- Standardizes player identity across datasets  

### Metrics Engine
- Offensive Value (OV): weighted run contribution metric (wOBA-inspired)  
- OV/PA: efficiency per plate appearance  
- Hit Rate / XBH Rate / Out Rate: player profile indicators  

### Player Archetypes
Classifies hitters into roles such as:
- Table Setter  
- Run Producer  
- Power Hitter  
- High Floor / Low Efficiency  

### Lineup Optimization
Builds a 12-player batting order based on:
- Efficiency  
- Role fit  
- Lineup balance  

### Simulation Engine
- Monte Carlo simulation (1000 games)  
- Models each plate appearance probabilistically  
- Tracks base advancement and scoring  
- Outputs:
  - Average runs  
  - Min / max range  
  - Median runs  

---

## Example Output

### Batting Order

1. Corey Moyer — Table Setter (OV/PA: 1.82)  
2. Matt Martiny — Table Setter (OV/PA: 1.79)  
3. Corbin Pierson — Run Producer (OV/PA: 1.75)  

---

### Team Analysis

Strengths:
- Strong contact hitting across lineup
- High overall offensive efficiency

Weaknesses:
- Bottom of lineup shows production drop-off

Key Insight:
- Matt Martiny is the most efficient hitter and should be placed in a high-impact spot (2–4)

---

### Run Projection

Optimized Lineup: 19.4 runs/game  
User Lineup: 17.8 runs/game  
Difference: +1.6 runs/game  

---

## Tech Stack

### Frontend
- React (Vite)  
- Recharts  
- Custom CSS  

### Backend
- FastAPI (Python)  
- Pandas / NumPy  

### Deployment
- Render (backend API)  
- Plesk (frontend hosting)  

---

## Project Structure

src/
  api.py                # FastAPI endpoints
  analyzer.py           # Analysis pipeline
  load_gamechanger.py   # CSV ingestion & normalization
  metrics.py            # Player metric calculations
  archetypes.py         # Player classification
  team_optimizer.py     # Batting order logic
  simulator.py          # Run simulation engine
  report.py             # Team insights

---

## Running Locally

pip install -r requirements.txt  
python src/main.py  

---

## Why This Matters

This project mirrors real analytics workflows:

- Data cleaning and normalization  
- Metric engineering  
- Player segmentation  
- Optimization modeling  
- Simulation-based decision making  

It demonstrates the ability to move from raw data to insights to interactive decision tools.

---

## Author

Matt Martiny  
Kansas City, KS
