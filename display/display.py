from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.columns import Columns
from rich.table import box

class RoguelikeConsoleDisplay:
    def __init__(self, live):
        self._live = live

    # Display current state of the game: map and information about players
    def display(self, view):
        self._live.update(Group(
            RoguelikeConsoleDisplay._render_map(view['map']),
            RoguelikeConsoleDisplay._render_players(view['character'], view['mobs'])    
        ), refresh=True)
    
    @staticmethod
    def _render_map(map_view):
        title = Panel(Text(f'Level {map_view["info"]["level"]}', style='bold cyan'))
        table = Table(title=title, show_header=False, show_lines=True)
        for _ in range(len(map_view['grid'][0])):
            table.add_column(justify='full', min_width=2)

        for row in map_view['grid']:
            table.add_row(*map(RoguelikeConsoleDisplay._render_map_cell, row))

        return table
    
    @staticmethod
    def _render_map_cell(cell):
        match cell:
            case '$': return ':trophy:'
            case '#': return ':construction:'
            case 'dagger': return ':dagger:'
            case 'shield': return ':shield:'
            case 'C': return ':person_walking:'
            case _: return cell

    @staticmethod
    def _render_players(character_view, mobs_view):
        s = character_view['stats']
        table = Table(title=':person_walking:', title_style='', show_header=False, box=box.SIMPLE_HEAD)
        table.add_column()
        table.add_column()
        table.add_row(':heart:', str(s['health']))
        table.add_row(':kitchen_knife:', str(s['attack']))
        table.add_row(':helmet_with_white_cross:', str(s['defense']))
        table.add_row(':crown:', str(s['experience']))
        
        return Columns([Panel(table)], expand=False)