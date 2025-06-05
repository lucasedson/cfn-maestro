import asyncio
from rich.console import Group, Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from datetime import datetime
import threading
import platform
console = Console()
stop_event = asyncio.Event()

def listen_for_q():
    system = platform.system()
    
    if system == "Windows":
        import msvcrt
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == 'q':
                    asyncio.run_coroutine_threadsafe(stop_event.set(), asyncio.get_event_loop())
                    break
    else:
        import sys
        import termios
        import tty
        import select
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                if stop_event.is_set():
                    break
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    ch = sys.stdin.read(1)
                    if ch.lower() == 'q':
                        asyncio.run_coroutine_threadsafe(stop_event.set(), asyncio.get_event_loop())
                        break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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


async def watch_shell_command(cmd: str, interval: float = 1.0):
    output_lines = []
    spinner = Spinner("dots", text="Watching... (press 'q' to quit)", style="cyan")

    def render():
        return Group(
            spinner,
            Text(f"[blue]Last updated:[/] {datetime.now().strftime('%H:%M:%S')}"),
            Panel("\n".join(output_lines[-20:]), title="Output", border_style="cyan")
        )

    # Inicia o escutador de teclado em uma thread separada
    threading.Thread(target=listen_for_q, daemon=True).start()

    with Live(render(), console=console, refresh_per_second=4) as live:
        while not stop_event.is_set():
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            output_lines.append(f"[blue]>>> Executing: {cmd} <<<[/blue]")

            while True:
                line = await process.stdout.readline()
                if not line or stop_event.is_set():
                    break
                output_lines.append(line.decode(errors="replace").rstrip())
                live.update(render())

            await process.wait()
            output_lines.append(f"[green]✔ Done ({process.returncode})[/green]\n")
            live.update(render())

            if stop_event.is_set():
                break

            await asyncio.sleep(interval)

    console.print("[bold yellow]⏹ Stopped...[/]")# Exemplo:
async def main():
    await run_shell_command('ping 8.8.8.8')

if __name__ == '__main__':
     run_async_task(watch_shell_command('dir', interval=5.0))