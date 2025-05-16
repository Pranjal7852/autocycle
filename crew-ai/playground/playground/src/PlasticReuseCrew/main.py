from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from plastic_brand_flow import PlasticBrandFlow
import asyncio
import json
from pathlib import Path
import logging
from dotenv import load_dotenv
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Store flow states using state_id as key
flow_states = {}

# Persistence directory
PERSISTENCE_DIR = Path("flow_results")
PERSISTENCE_DIR.mkdir(exist_ok=True)

class UserInput(BaseModel):
    brand_name: str
    plastic_type: str
    location: str

class HumanInputRequest(BaseModel):
    state_id: str
    selected_brand: str

@app.post("/start")
async def start_flow(user_input: UserInput):
    flow_states_tmp = {}  # Temporary storage until state_id is available
    flow = PlasticBrandFlow(flow_states=flow_states_tmp)

    async def run_flow():
        try:
            result = await flow.kickoff_async(inputs=user_input.dict())
            flow_states_tmp[flow.state.id]["result"] = result
            if result:
                with open(PERSISTENCE_DIR / f"{flow.state.id}.json", "w") as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Flow with State ID {flow.state.id} result persisted")
        except Exception as e:
            logger.error(f"Flow with State ID {flow.state.id} failed: {str(e)}")
            flow_states_tmp[flow.state.id]["result"] = {"error": str(e)}

    task = asyncio.create_task(run_flow())
    try:
        await asyncio.wait([task], timeout=1.0)
    except asyncio.TimeoutError:
        pass

    # Wait for state_id to be available
    state_id = flow.state.id
    flow_states[state_id] = flow_states_tmp.get(state_id, {
        "prompt": None,
        "brands": None,
        "input": None,
        "event": asyncio.Event(),
        "result": None,
        "state_id": state_id
    })
    del flow_states_tmp

    for _ in range(10):  # Timeout after ~5 seconds
        await asyncio.sleep(0.5)
        if flow_states[state_id]["prompt"] and flow_states[state_id]["state_id"]:
            break
    else:
        if flow_states[state_id].get("result", {}).get("error"):
            raise HTTPException(status_code=500, detail=flow_states[state_id]["result"]["error"])
        raise HTTPException(status_code=500, detail="Failed to generate brand list")

    logger.info(f"Flow with State ID {state_id} waiting for human input")
    return {
        "status": "waiting_for_human",
        "state_id": state_id,
        "prompt": flow_states[state_id]["prompt"],
        "brands": flow_states[state_id]["brands"]
    }

@app.post("/human-input")
async def submit_input(request: HumanInputRequest):
    state_id = request.state_id
    if state_id not in flow_states:
        raise HTTPException(status_code=404, detail="Flow not found")
    if not request.selected_brand:
        raise HTTPException(status_code=400, detail="Selected brand is required")

    logger.info(f"Flow with State ID {state_id} received human input: {request.selected_brand}")
    flow_states[state_id]["input"] = request.selected_brand
    flow_states[state_id]["event"].set()

    for _ in range(20):  # Timeout after ~10 seconds
        await asyncio.sleep(0.5)
        if flow_states[state_id].get("results") is not None:
            break
    else:
        raise HTTPException(status_code=500, detail="Flow did not complete")

    result = flow_states[state_id]["result"]
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    logger.info(f"Flow with State ID {state_id} completed")
    del flow_states[state_id]
    return {"status": "completed", "state_id": state_id, "result": result}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plastic Brand Flow</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex items-center justify-center h-screen">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
            <h1 class="text-2xl font-bold mb-4">Plastic Brand Flow</h1>
            <div id="input-form">
                <div class="mb-4">
                    <label class="block text-sm font-medium">Brand Name</label>
                    <input id="brand_name" type="text" class="w-full p-2 border rounded">
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium">Plastic Type</label>
                    <input id="plastic_type" type="text" class="w-full p-2 border rounded">
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium">Location</label>
                    <input id="location" type="text" class="w-full p-2 border rounded">
                </div>
                <button onclick="startFlow()" class="w-full bg-blue-500 text-white p-2 rounded">Start Flow</button>
            </div>
            <div id="brand-selection" class="hidden">
                <p id="prompt" class="mb-4"></p>
                <select id="brand_list" class="w-full p-2 border rounded mb-4"></select>
                <button onclick="submitBrand()" class="w-full bg-green-500 text-white p-2 rounded">Submit Selection</button>
            </div>
            <div id="result" class="hidden mt-4"></div>
        </div>
        <script>
            let stateId = null;

            async function startFlow() {
                const brand_name = document.getElementById("brand_name").value;
                const plastic_type = document.getElementById("plastic_type").value;
                const location = document.getElementById("location").value;

                const response = await fetch("/start", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ brand_name, plastic_type, location })
                });
                const data = await response.json();

                if (data.status === "waiting_for_human") {
                    stateId = data.state_id;
                    document.getElementById("prompt").innerText = data.prompt + `\n\nState ID: ${stateId}`;
                    const brandList = document.getElementById("brand_list");
                    brandList.innerHTML = data.brands.map(brand => `<option value="${brand}">${brand}</option>`).join("");
                    document.getElementById("input-form").classList.add("hidden");
                    document.getElementById("brand-selection").classList.remove("hidden");
                }
            }

            async function submitBrand() {
                const selected_brand = document.getElementById("brand_list").value;
                const response = await fetch("/human-input", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ state_id: stateId, selected_brand })
                });
                const data = await response.json();

                if (data.status === "completed") {
                    document.getElementById("brand-selection").classList.add("hidden");
                    const resultDiv = document.getElementById("result");
                    resultDiv.classList.remove("hidden");
                    resultDiv.innerHTML = `<h2 class="text-xl font-bold">Result (State ID: ${data.state_id})</h2><pre>${JSON.stringify(data.result, null, 2)}</pre>`;
                }
            }
        </script>
    </body>
    </html>
    """