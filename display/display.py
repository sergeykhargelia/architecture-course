import os

from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.columns import Columns
from rich.table import box

class RoguelikeConsoleDisplay:
    def __init__(self, live):
        self._live = live

    # Display the current state of the game: map and information about players
    def display_game_state(self, view):
        self._live.update(Group(
            RoguelikeConsoleDisplay._render_map(view['map']),
            RoguelikeConsoleDisplay._render_players([view['character']] + view['mobs'])    
        ), refresh=True)

    # Display the lose banner
    def display_lose(self):
        with open(os.path.join('assets', 'lose.txt')) as f:
            text = Text(f.read(), style='bold red')
            self._live.update(Panel(text, expand=False), refresh=True)

    # Display the win banner
    def display_win(self):
        with open(os.path.join('assets', 'win.txt')) as f:
            text = Text(f.read(), style='bold green')
            self._live.update(Panel(text, expand=False), refresh=True)
    
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
        def render_cell_part(part):
            match part:
                case '$': return ':trophy:'
                case '#': return ':construction:'
                case 'dagger': return ':dagger:'
                case 'shield': return ':shield:'
                case 'C': return ':person_walking:'
                case 'mob1': return ':space_invader:'
                case 'mob2': return ':ogre:'
                case 'mob3': return ':robot:'
                case 'mob4': return ':alien:'
                case _: return part

        return ' '.join(map(render_cell_part, cell.split(',')))

    @staticmethod
    def _render_stat_component(name):
        match name:
            case 'health': return ':heart:'
            case 'attack': return ':kitchen_knife:'
            case 'defense': return ':helmet_with_white_cross:'
            case 'experience': return ':crown:'

    @staticmethod
    def _render_players(players_view):
        def generate_table(player_view):
            s = player_view['stats']
            table = Table(
                title=RoguelikeConsoleDisplay._render_map_cell(player_view['name']), 
                title_style='', show_header=False, box=box.SIMPLE_HEAD
            )
            table.add_column()
            table.add_column()
            
            for key in s.keys():
                table.add_row(RoguelikeConsoleDisplay._render_stat_component(key), str(s[key]))

            return table

        tables = list(map(lambda view: Panel(generate_table(view)), players_view))
        return Columns(tables, expand=False)