from .common.server import create_app
from .agents.task_manager import run

app = create_app(agent=type("Agent", (), {"execute": run}))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)