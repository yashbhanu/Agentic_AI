from .agent import execute
async def run(payload, uid):
    return await execute(payload, uid)