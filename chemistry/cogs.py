from typing import Dict, Tuple
from random import randint
from timeit import default_timer

from discord import Message, Embed, Colour
from discord.ext.commands import Cog, Bot, command, Context

from .solvers.solver_base_class import ChemistrySolverBaseClass
from .solvers.solver_periodni import _OxidationNumberAssignment, _SimpleBalance, _RedoxBalance
from .solvers.solver_chemequations import _ReactionPrediction

_CHEMISTRY_COMMANDS: Dict[str, Dict[str, str]] = {}
_COGS = []

class ChemistryCogs(Cog):
    def __init__(self, bot: Bot, solver: ChemistrySolverBaseClass=None) -> None:
        self.bot = bot
        self.solver = solver

    def __init_subclass__(cls) -> None:
        info = cls.commands_info()
        _COGS.append(cls)
        if info:
            for key in info.keys():
                if key not in _CHEMISTRY_COMMANDS:
                    _CHEMISTRY_COMMANDS[key] = info[key]
        return super().__init_subclass__()
    
    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return dict()
    
    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        message: Message = ctx.message
        await message.remove_reaction('⌛', self.bot.user)
        await message.add_reaction('👌', self.bot.user)
        await message.add_reaction('⚠')
        await ctx.send(f'> {ctx.message.content}\n{error}')
    
    async def cog_before_invoke(self, ctx: Context) -> None:
        message: Message = ctx.message
        await message.add_reaction('⌛')

    async def cog_after_invoke(self, ctx: Context) -> None:
        message: Message = ctx.message
        await message.remove_reaction('⌛', self.bot.user)
        await message.add_reaction('👌')
    
    
class ONAssignment(ChemistryCogs):
    def __init__(self, bot) -> None:
        super().__init__(bot, _OxidationNumberAssignment())

    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return {
            'on': {
                'alias': tuple(),
                'syntax': 'on `compound1` `compound2` `compound3` `...`',
                'description abbr': 'Takes chemical compounds, and returns the oxidation number of each elements.',
                'description': '''Takes chemical compounds and return the oxidation number of each elements.

                This command take, at least, one chemical `compound`.
                Compounds should be seperated by spaces.
                
                Example: 
                ```#on Ca2+ HF2^- Fe4[Fe(CN)6]3 NH4NO3 so42- ch3cooh cuso4*5h2o```'''
            }
        }

    @command(name='on')
    async def multi(self, ctx: Context, compound: str, *args) -> None:
        result = self.solver.solve(compound, *args)
        await ctx.send(embed=result)


class SimpleBalance(ChemistryCogs):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _SimpleBalance())

    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return {
            'balance': {
                'alias': ('bal',),
                'syntax': 'bal `"reactants"` `"products"`',
                'description abbr': 'Takes reactants and products, returns the balanced reaction.',
                'description': '''This command take two arguments.
                The first argument is the `reactants` and the second is the `products`.
                Both argument should be inside of `\"\"` and seperated by a space.
                Valid seperators for the reactants and products are `,` `+` and ` `(space).
                Example: 
                ```balance "Ca3(PO4)2 H2SO4" "H3PO4, CaSO4"```'''
            },
            'balancemany': {
                'alias': ('balmany', 'balm'),
                'syntax': 'balancemany `"reaction1"` `"reaction2"` `"reaction3"` `...`',
                'description abbr': 'Takes multiple chemical reactions, returns the balanced reactions.',
                'description': '''Similar to the `balance` command, but instead of taking reactants and products,
                this command takes, at least, one `chemical reaction`.
                Each reaction should be inside of `\"\"`. Reactions should be seperated by spaces.
                Valid seperators for the reactants and products are `,` `+` and ` `(space).
                Reactants and products should be seperated by an `=`.
                Example:
                ```balancemany "Ca3(PO4)2 H2SO4 = H3PO4, CaSO4" "SiCl4 + H2O=SiO2 + HCl"```
                '''
            }
        }


    @command(name='balance', aliases=['bal'])
    async def single(self, ctx: Context, reactants: str, products: str) -> None:
        result = self.solver.solve((f'{reactants}={products}',))
        await ctx.send(embed=result)
    
    @command(name='balancemany', aliases=['balmany', 'balm'])
    async def multi(self, ctx: Context, reaction: str, *args) -> None:
        result = self.solver.solve((reaction, *args))
        await ctx.send(embed=result)


class RedoxBalance(ChemistryCogs):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _RedoxBalance())

    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return {
            'redox': {
                'alias': ('re',),
                'syntax': 'redox `"median"` `"reactants"` `"products"`',
                'description abbr': 'Takes median, reactants, and products, returns the balanced redox reaction.',
                'description': '''This command take three arguments.
                The first argument is the `median` in which the reaction occurs.
                Median can either a (A)cidic or (B)asic.
                The second and third are the `reactants` and the `products`.
                All argument should be inside of `\"\"` and seperated by spaces.
                Valid seperators for the reactants and products are `,` `+` and ` `(space).
                Example: 
                ```redox "a" "HIO3, FeI2 HCl" "FeCl3 + ICl + H2O"```'''
            },
            'redoxmany': {
                'alias': ('remany', 'rem'),
                'syntax': 'balancemany `"median1 reaction1"` `"median2 reaction2"` `"median3 reaction3"` `...`',
                'description abbr': 'Takes multiple median and reations, returns the balanced redox reactions.',
                'description': '''A multiple version of the `redox` command.
                Each argument consists of 2 parts. The first is the `median` and the second is the `reaction` itself.
                The median and reaction should be inside of \"\" and seperated by a space.
                The reaction consist of `reactants` and `products`, seperated by `=`.
                Valid seperators for the reactants and products are `,` `+` and ` `(space).
                Example:
                ```redoxmany "a HIO3, FeI2 HCl=FeCl3 + ICl + H2O" "basic CuSCN, KIO3, HCl=CuSO4 KCl HCN ICl H2O"```
                '''
            }
        }
    
    @command(name='redox', aliases=['re'])
    async def single(self, ctx: Context, median: str, reactants: str, products: str) -> None:
        result = self.solver.solve(((median, f'{reactants}={products}'),))
        await ctx.send(embed=result)

    @command(name='redoxmany', aliases=['remany', 'rem'])
    async def multi(self, ctx: Context, reaction: str, *args) -> None:
        reactions = []
        for reaction in (reaction, *args):
            m, r = reaction.split(maxsplit=1)
            reactions.append((m.strip(), r.strip()))
        result = self.solver.solve(tuple(reactions))
        await ctx.send(embed=result)


class ReactionPrediction(ChemistryCogs):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _ReactionPrediction())

    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return {
            'predict': {
                'alias': ('pred',),
                'syntax': 'predict `"reactants"` `"product"` `page number`',
                'description abbr': 'Takes reactants and products, returns reactions include said reactants and products.',
                'description': '''This command takes either `reactants` or `products`.
                To leave a field empty, simple enter the argument as `""`.
                Valid seperators for the reactants and products are `,` `+` and ` `(space).
                Page number defaults to 1, which means this field can be left empty, but cannot be less than 1.
                Example:
                ```predict "H2O"\npredict "" "CO2 H2O"\npredict "O2" "CO2, H2O"\npredict "O2" "O3" 4```'''
            }
        }
    
    @command(name='predict', aliases=['pred'])
    async def single(self, ctx: Context, reactants: str='', products: str='', page: int=1) -> None:
        result = self.solver.solve(reactants, products, page)
        await ctx.send(embed=result)


class HelpCommand(ChemistryCogs):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @staticmethod
    def commands_info() -> Dict[str, Dict[str, str]]:
        return {}

    @staticmethod
    def _help_embed() -> Embed:
        embed = Embed(title="Available commands", color=Colour.blue())
        for cmd_name in _CHEMISTRY_COMMANDS.keys():
            if cmd_name == 'help':
                continue
            info = _CHEMISTRY_COMMANDS[cmd_name]
            description = info.get('description abbr', '')
            embed.add_field(name=cmd_name, value=description, inline=False)
        return embed
    
    @staticmethod
    def _command_embed(
        cmd_name: str, 
        aliases: Tuple[str],
        syntax: str, 
        description: str
    ) -> Embed:
        embed = Embed(title=cmd_name, color=Colour.blue())

        alias = ', '.join(aliases)
        if alias:
            embed.add_field(name='Aliases', value=alias, inline=False)
        if syntax:
            embed.add_field(name='Syntax', value=syntax, inline=False)
        if description:
            embed.add_field(name='Description', value=description, inline=False)
        return embed

    @command(name='help')
    async def _help(self, ctx: Context, cmd_name: str=None) -> None:
        if not cmd_name:
            await ctx.send(embed=self._help_embed())
        elif cmd_name in _CHEMISTRY_COMMANDS:
            info_dict = _CHEMISTRY_COMMANDS[cmd_name]
            embed = self._command_embed(
                cmd_name,
                info_dict.get('alias', ''),
                info_dict.get('syntax', ''),
                info_dict.get('description', '')
                )
            await ctx.send(embed=embed)
        elif cmd_name == 'help':
            raise NotImplemented()
        else:
            raise ValueError("Unknown command name")

    @command(name='cake')
    async def bake_a_cake(self, ctx: Context) -> None:
        timer_start = default_timer()
        embed = Embed(
            title='Balanced 🍰 of 🍰 Reaction(s).',
            color=Colour.from_rgb(255,119,188)
        )
        embed.add_field(
            name=f'{randint(1, 8)}🌾 + {randint(2, 6)}🥚 + {randint(2, 10)}🍫 = {randint(2,4)}🎂',
            value='Orignal: ```Cake```',
            inline=False
            )
        embed.add_field(
            name='Status',
            value=f'✅ Success (100.0%)',
            inline=False
            )
        embed.add_field(
            name='Inputs',
            value='" **cake** "',
            inline=False
            )
        embed.add_field(
            name='Interpreted as',
            value='" **🎂** "',
            inline=False
            )
        timer_end = default_timer()
        embed.add_field(
            name='Finished in',
            value=f'{timer_end-timer_start:.2f}s',
            inline=False
            )
        await ctx.message.add_reaction('🎉')
        await ctx.send(embed=embed)

def setup(bot):
    for cog in _COGS:
        bot.add_cog(cog(bot))
