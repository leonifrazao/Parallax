from rich.console import Console
from rich.table import Table
from typing import Iterable

from parallax.models import Narrative
from parallax.interfaces.out.ICliApp import ICliApp


class CliApp(ICliApp):
    def __init__(self):
        self.console = Console()

    def render_narratives(self, narratives: Iterable[Narrative]) -> None:
        table = Table(title="Narrative Analysis", show_lines=True)

        table.add_column("ID", style="dim", overflow="fold")
        table.add_column("Headline", style="bold", overflow="fold")
        table.add_column("Stance")
        table.add_column("Tone")
        table.add_column("Intensity", justify="right")
        table.add_column("Source", overflow="fold")
        table.add_column("URL", overflow="fold")

        for narrative in narratives:
            table.add_row(
                narrative.id,
                narrative.headline,
                narrative.stance,
                narrative.emotional_tone,
                f"{narrative.emotional_intensity:.2f}",
                narrative.source,
                narrative.url,
            )

        self.console.print(table)