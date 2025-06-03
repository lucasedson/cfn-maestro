import asyncio
async def run_shell_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode(errors="replace").rstrip())

    await process.wait()
def run_async_task(task):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(task)
    finally:
        loop.close()

# Exemplo:
async def main():
    await run_shell_command('ls -la | grep .py')

if __name__ == '__main__':
    asyncio.run(main())
