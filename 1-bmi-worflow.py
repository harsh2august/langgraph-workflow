from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import base64
import requests
from IPython.display import Image, display

# 1. Define State
class BMIState(TypedDict):
    weight_kg: float
    height_kg: float
    bmi: float
    category: str

# 2. Define Nodes (Added 'return state' to label_bmi)
def calculate_bmi(state: BMIState) -> BMIState:   
    weight = state['weight_kg']
    height = state['height_kg']
    bmi = weight / (height**2)
    state['bmi'] = round(bmi, 2)
    return state

def label_bmi(state: BMIState) -> BMIState:
    bmi = state['bmi']
    if bmi < 18.5:
        state["category"] = "Underweight"
    elif 18.5 <= bmi < 25:
        state["category"] = "Normal"
    elif 25 <= bmi < 30:
        state["category"] = "Overweight"
    else:
        state["category"] = "Obese"
    return state

# 3. Build Graph
graph = StateGraph(BMIState)
graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi', label_bmi)

graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'label_bmi')
graph.add_edge('label_bmi', END)

workflow = graph.compile()

# 4. Execute
initial_state = {'weight_kg': 72, 'height_kg': 1.83}
final_state = workflow.invoke(initial_state)
print(f"BMI: {final_state['bmi']} | Category: {final_state['category']}")

#generate worflow image
def save_graph_image(compiled_graph, filename="graph.png"):
    # 1. Get the Mermaid syntax
    mermaid_markup = compiled_graph.get_graph().draw_mermaid()
    
    # 2. Encode it for the Mermaid.ink API
    encoded = base64.b64encode(mermaid_markup.encode('ascii')).decode('ascii')
    url = f'https://mermaid.ink/img/{encoded}'
    
    # 3. Download the image bytes
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 4. Write bytes to a local file
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Success! Workflow image saved as: {filename}")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
save_graph_image(workflow)

#graph ke input me v state dete hain and execute ke baad waaps wo state object hi deta hai.
#we can create workflow graph image via IPythhon