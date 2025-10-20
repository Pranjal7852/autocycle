# Autocycle – Turning Waste Into Brand Value

## Table of Contents
1. [Overview](#overview)
2. [Backend Documentation](#backend-documentation)
   - [Architecture](#backend-architecture)
   - [Setup](#backend-setup)
   - [API Structure](#api-structure)
   - [AI Integration](#ai-integration)
3. [Frontend Documentation](#frontend-documentation)
   - [Architecture](#frontend-architecture)
   - [Setup](#frontend-setup)
   - [Components](#frontend-components)

---

## Overview

**Closing the Loop Through Collaboration**  
Waste isn’t worthless — it’s untapped brand value.  

Autocycle connects **brands generating post-consumer plastic waste** with **companies sourcing recycled materials**.  
Through **AI-driven matching, collaboration, and co-branding**, we help raise recycling rates, ensure high-quality material supply, and make dismantling financially worthwhile.  

Our mission:  
> “Turn waste streams into stories of innovation and circular value.”

## ⚙️ How It Works

Autocycle makes circular collaboration **simple, fast, and transparent**.

1. **Fill the form about Waste Data**  
   Share your post-consumer, excess, or overstock plastics.  
2. **AI Material Matching**  
   Our AI matches your materials with potential buyers — optimized for recyclability, location, and cost.  
3. **Connect with Decision Makers**  
   Skip the months of outreach. We bring you directly to verified partners.  
4. **Co-Create & Scale**  
   Align on supply and branding — recyclers and compounders join in to make it real.  

Wherever you are, Autocycle connects the dots to turn waste into value — **making dismantling worth it** and **sourcing sustainable**.

## Backend Documentation

### Backend Architecture
The backend is built using:
- **FastAPI**: Modern, fast web framework for building APIs
- **CrewAI**: AI agent framework for brand analysis
- **PostgreSQL**: Primary database
- **Weaviate**: Vector database for semantic search
- **Docker**: Containerization

#### Key Components:
1. **AI Crews and Flows**:
   - **Brand Research Flow**
     - Brand Collaboration Crew
       - Analyzes brand compatibility
       - Generates collaboration insights
       - Provides strategic recommendations
     - Tools:
       - Brand analysis tools
       - Market research tools
       - Collaboration assessment tools

   - **Brand Product Flow**
     - Product Ideas Crew
       - Generates collaborative product concepts
       - Creates detailed product descriptions
       - Provides visual guidance for AI image generation
     - Brand Product Analysis Crew
       - Analyzes product-market fit
       - Evaluates brand alignment
       - Provides implementation recommendations

   - **Plastic Analysis Flow**
     - Material Analysis Crew
       - Analyzes plastic materials
       - Provides sustainability insights
       - Recommends material applications
     - Environmental Impact Crew
       - Evaluates environmental impact
       - Suggests sustainable alternatives
       - Provides compliance recommendations

2. **Database Structure**:
   - PostgreSQL for structured data
   - Weaviate for vector embeddings and semantic search

### Flow Architecture

#### Brand Research Flow
The Brand Research Flow is responsible for analyzing and evaluating potential brand collaborations:

1. **Main Components**:
   - `main.py`: Entry point for brand research flow
   - `crews/brand_collab/`: Brand collaboration analysis
   - `tools/`: Custom tools for brand analysis

2. **Process Flow**:
   ```
   Input → Brand Analysis → Collaboration Assessment → Strategic Recommendations → Output
   ```

3. **Key Features**:
   - Brand compatibility analysis
   - Market research integration
   - Strategic recommendation generation
   - Collaboration opportunity identification

#### Brand Product Flow
The Brand Product Flow handles product ideation and analysis:

1. **Main Components**:
   - Product idea generation
   - Product analysis
   - Visual concept development

2. **Process Flow**:
   ```
   Input → Product Ideation → Market Analysis → Visual Concept → Final Output
   ```

3. **Key Features**:
   - Collaborative product concept generation
   - Market fit analysis
   - Visual concept development
   - Implementation planning

#### Plastic Analysis Flow
The Plastic Analysis Flow focuses on material analysis and sustainability:

1. **Main Components**:
   - Material analysis
   - Environmental impact assessment
   - Sustainability recommendations

2. **Process Flow**:
   ```
   Input → Material Analysis → Environmental Assessment → Sustainability Planning → Output
   ```

3. **Key Features**:
   - Material property analysis
   - Environmental impact evaluation
   - Sustainability recommendations
   - Compliance checking

### Crew Architecture

Each crew is designed with specific roles and responsibilities:

1. **Brand Collaboration Crew**:
   ```python
   class BrandCollaborationCrew:
       - Brand Analyst Agent
       - Market Research Agent
       - Strategy Advisor Agent
   ```

2. **Product Ideas Crew**:
   ```python
   class ProductIdeasCrew:
       - Product Conceptualizer Agent
       - Market Analyst Agent
       - Visual Designer Agent
   ```

3. **Material Analysis Crew**:
   ```python
   class MaterialAnalysisCrew:
       - Material Scientist Agent
       - Environmental Analyst Agent
       - Sustainability Advisor Agent
   ```

### Integration Points

1. **Flow Integration**:
   - Flows are orchestrated through the main FastAPI application
   - Each flow can be triggered independently or as part of a larger process
   - Results are stored in both PostgreSQL and Weaviate for different use cases

2. **Crew Communication**:
   - Crews communicate through structured data formats
   - Results are passed between crews using Pydantic models
   - Logging and monitoring are implemented at each step

3. **Data Flow**:
   ```
   Input Data → Flow Orchestration → Crew Execution → Data Storage → API Response
   ```

### Backend Setup

#### Prerequisites:
- Python 3.11+
- PostgreSQL
- Docker (for Weaviate)
- Node.js 16+ (for frontend)

#### Installation Steps:
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd batch23-bmw
   ```

2. **Set up Python environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the backend directory:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   WEAVIATE_URL=http://localhost:8080
   OPENAI_API_KEY=your_api_key
   ```

4. **Start Postgress**:
   ```bash
   docker compose up -d
   ```

### API Structure

#### Main Endpoints:
1. **Brand Analysis**:
   - `/generateBrand`: Analyze brand data and plastic data to give 5 real potential brand for Brand Collaboration.  

2. **Product Ideas**:
   - `/generateproducts`: Generate product ideas for provided brands and plastic type. Given visual images and pitch text.


### AI Integration

#### CrewAI Agents:
1. **Brand Analyst**:
   - Analyzes brand data
   - Generates brand insights
   - Provides strategic recommendations

2. **Product Ideas Generator**:
   - Creates collaborative product concepts
   - Generates detailed product descriptions
   - Provides visual guidance for AI image generation

3. **Plastic Analyst**:
   - Analyzes plastic materials
   - Provides sustainability insights
   - Recommends material applications

## Frontend Documentation

### Frontend Architecture
The frontend is built using:
- **React**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first CSS framework

### Frontend Setup

#### Installation:
```bash
cd frontend/Autocycle_final
pnpm install  # or npm install
```

#### Development:
```bash
pnpm dev  # or npm run dev
```

### Frontend Components

#### Main Components:
1. **Landing Page**:
   - Brand introduction
   - Project overview
   - Navigation

2. **Brand Analysis**:
   - Brand input form
   - Analysis results display
   - Interactive visualizations

3. **Product Ideas**:
   - Product concept display
   - Interactive product viewer
   - Collaboration interface

4. **Material Analysis**:
   - Material properties display
   - Sustainability metrics
   - Comparison tools

### Live Demo:
- [Final Product Show at DPS Munich](https://youtu.be/qolmGCnjg_4)