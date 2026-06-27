# 🤖 AI Recruiter Outreach Agent

> **An AI-powered multi-agent recruitment outreach platform that
> researches companies, matches portfolio projects, generates
> personalized recruiter emails, and creates Gmail drafts with resume
> attachments.**

------------------------------------------------------------------------

# Overview

AI Recruiter Outreach Agent automates the repetitive parts of recruiter
outreach while keeping a human-in-the-loop before emails are sent.

Instead of sending generic cold emails, the platform:

-   Researches the target company
-   Understands its technology stack and hiring focus
-   Matches the most relevant projects from the candidate portfolio
-   Generates a personalized outreach email
-   Stores drafts in MySQL
-   Creates Gmail drafts with resume attachments

------------------------------------------------------------------------

# Problem Statement

Job seekers often spend hours:

-   Researching companies
-   Customizing resumes
-   Selecting projects
-   Writing personalized emails

This project automates those repetitive tasks using specialized AI
agents.

------------------------------------------------------------------------

# Key Features

-   Multi-Agent AI architecture
-   Company research using SerpAPI + LLM
-   Structured company metadata extraction
-   Local JSON caching to reduce API costs
-   Intelligent portfolio project matching
-   Personalized recruiter email generation
-   MySQL persistence
-   Gmail Draft creation via Gmail API
-   Resume attachment support
-   Modular FastAPI-ready architecture

------------------------------------------------------------------------

# System Architecture

``` text
Recruiter Database
        │
        ▼
Company Research Agent
        │
        ▼
Company Cache
        │
        ▼
Project Matching Agent
        │
        ▼
Email Generation Agent
        │
        ▼
Resume Service
        │
        ▼
Gmail Draft Service
        │
        ▼
Draft saved in Gmail
```

------------------------------------------------------------------------

# Multi-Agent Workflow

## 1. Company Research Agent

Responsibilities

-   Search company information
-   Extract:
    -   Industry
    -   Domain
    -   Tech Stack
    -   Hiring Focus
    -   Keywords
    -   Company Summary

Uses:

-   SerpAPI
-   Groq LLM
-   JSON Cache

------------------------------------------------------------------------

## 2. Project Matching Agent

Inputs

-   Company metadata
-   Candidate project catalog

Outputs

-   Top relevant projects
-   Matching reason

Uses semantic reasoning to explain why each project is relevant.

------------------------------------------------------------------------

## 3. Email Generation Agent

Uses

-   Recruiter information
-   Company analysis
-   Candidate profile
-   Matched projects
-   Matching reason

Generates a personalized recruiter outreach email in JSON format.

------------------------------------------------------------------------

## 4. Gmail Service

Creates Gmail drafts using OAuth2.

Features:

-   Draft creation
-   Resume attachment
-   Human review before sending

------------------------------------------------------------------------

# Complete Workflow

``` text
Recruiter
    │
    ▼
Company Research
    │
    ▼
Company Cache
    │
    ▼
Project Matching
    │
    ▼
Email Generation
    │
    ▼
Save to MySQL
    │
    ▼
Create Gmail Draft
    │
    ▼
Review
    │
    ▼
Send
```

------------------------------------------------------------------------

# Database Design

## recruiters

  Column
  ---------
  id
  name
  company
  title
  email

## generated_emails

  Column
  ------------------
  id
  recruiter_id
  subject
  body
  status
  company_analysis
  project_matching
  gmail_draft_id
  created_at

------------------------------------------------------------------------

# Tech Stack

## Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   MySQL

## AI

-   Groq LLM
-   Prompt Engineering
-   Pydantic

## APIs

-   Gmail API
-   SerpAPI

## Authentication

-   OAuth2

------------------------------------------------------------------------

# Project Structure

``` text
app/
│
├── agent/
│   ├── company_research_agent.py
│   ├── project_matching_agent.py
│   └── email_generation_agent.py
│
├── services/
│   ├── company_services.py
│   ├── gmail_services.py
│   ├── resume_services.py
│   ├── llm_services.py
│   ├── cache_services.py
│   └── outreach_pipeline_services.py
│
├── database/
├── prompts/
├── schemas/
├── data/
│   ├── resumes/
│   └── *.json
└── tests/
```

------------------------------------------------------------------------

# AI Pipeline

1.  Recruiter selected
2.  Company researched
3.  Cache checked
4.  Company metadata extracted
5.  Projects matched
6.  Personalized email generated
7.  Saved to MySQL
8.  Gmail draft created
9.  Resume attached
10. Human reviews before sending

------------------------------------------------------------------------

# Current Status

✅ Company Research Agent

✅ Company Cache

✅ Resume Knowledge Base

✅ Project Matching Agent

✅ Email Generation Agent

✅ Gmail Draft Integration

✅ Resume Attachment

✅ MySQL Storage

🚧 FastAPI Endpoints

🚧 Frontend Dashboard

🚧 Email Analytics

------------------------------------------------------------------------

# Future Roadmap

-   Web dashboard
-   Resume selection agent
-   Follow-up email generation
-   Recruiter reply analysis
-   Email quality scoring
-   OpenAI / Claude model support
-   Scheduling and automation
-   Analytics dashboard

------------------------------------------------------------------------

# Screenshots

Add screenshots here:

-   Architecture Diagram
-   Company Analysis Output
-   Project Matching Output
-   Generated Email
-   Gmail Draft
-   Dashboard

------------------------------------------------------------------------

# Author

**Rishu Kumar**

Built as a portfolio project demonstrating:

-   Agentic AI
-   LLM Engineering
-   Backend Development
-   Workflow Automation
-   Prompt Engineering
-   Gmail API Integration
-   Production-style software architecture

------------------------------------------------------------------------

# License

MIT License
