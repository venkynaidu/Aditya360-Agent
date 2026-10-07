from langchain_core.tools import tool
from university_data import DEPARTMENTS

@tool
def university_information(query:str)->str:
    """Use for university or department information."""
    if "department" in query.lower() or "branch" in query.lower():
        return "\n".join(f"{k}: {v}" for k,v in DEPARTMENTS.items())
    return "I can help with approved university information, departments, academics and campus guidance."

@tool
def course_guidance(topic:str)->str:
    """Use for courses, skills, learning roadmaps and department guidance."""
    q=topic.lower()
    if "python" in q: return "Python roadmap: fundamentals → functions → OOP → APIs → data → projects."
    if "ai" in q: return "AI roadmap: Python → maths/data → ML → deep learning → GenAI → RAG → agents → projects."
    return "Build fundamentals first, practise consistently, and finish with portfolio-ready projects."

@tool
def placement_guidance(target_role:str)->str:
    """Use for placement, career and employability guidance."""
    if "ai" in target_role.lower():
        return "AI career roadmap: Python + SQL + ML + GenAI/RAG + Git + deployable projects + aptitude + interviews."
    return "Placement roadmap: programming + DSA + SQL + Git + projects + aptitude + communication + mock interviews."

@tool
def study_plan(request:str)->str:
    """Use for personalized study planning."""
    return f"Goal: {request}\n• 20% concepts\n• 50% hands-on practice\n• 20% project/problem\n• 10% revision"

TOOLS=[university_information,course_guidance,placement_guidance,study_plan]
