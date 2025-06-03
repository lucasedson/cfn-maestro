import asyncio
from rich.console import Group, Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
console = Console()
async def run_shell_command(cmd: str):
    output_lines = []
    spinner = Spinner("dots", text="Running...", style="cyan")

    def render():
        return Group(
            spinner,
            Panel("\n".join(output_lines[-20:]), title="Running", border_style="cyan")
        )

    with Live(render(), console=console) as live:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            
        )
        out_cmd = f"[blue]Executing:[/blue] [b]{cmd}[/]"
        console.print(out_cmd)
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            decoded = line.decode(errors="replace").rstrip()
            output_lines.append(decoded)
            live.update(render())

        await process.wait()

        # Finalização com status
        if process.returncode == 0:
            live.update(
                Group(
                    Text("✅ Sucess!", style="green bold"),
                    Panel("\n".join(output_lines[-20:]), title="Output", border_style="green")
                )
            )
        else:
            live.update(
                Group(
                    Text("💥 Failed", style="red bold"),
                    Panel("\n".join(output_lines[-20:]), title="Erro", border_style="red")
                )
            )

def run_async_task(task):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(task)

# Exemplo:
async def main():
    await run_shell_command('ping 8.8.8.8')

if __name__ == '__main__':
    asyncio.run(main())
