# Google_ADK_FraudRiskToyAgent
A toy agent demonstrating use of AI Agents in Fraud Risk using Google ADK

# Agentic Fraud Risk – Toy Example

This repository demonstrates a minimal agentic AI system
for fraud risk assessment in banking.

## What this is
- Deterministic tools generate fraud risk signals
- A proxy model produces a risk score
- An LLM-based agent interprets signals and recommends action

## What this is NOT
- A production fraud system
- A full ML pipeline
- A real-time transaction engine

## Architecture
Transaction & Customer Data (Tool)
        -->
Fraud Model Proxy (Tool)
        -->
Agent Orchestrator
        -->
LLM Reasoning
        -->
Risk Rating & Action

## Why this matters
The model predicts risk.
The agent reasons about it.
