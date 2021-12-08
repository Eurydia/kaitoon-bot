# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, Context, command
from discord import Embed, Colour

from chemistry.cogs.cogs_base import ChemistryCogBase

from chemistry.cogs._help_info import COMMAND
from chemistry.cogs._errors_msg import KaitoonValueError


def _make_help_embed() -> Embed:
    embed = Embed(
        title="Available commands",
        description="""\
อ่านคู่มือภาษาไทย [[คลิก](https://meteor-danger-942.notion.site/a74699d7822e43529994d49f693cbeca)]
**Available prefixes**: "#", "]]"
**Note**: "`🧊`" represents one space.\
""",
        color=Colour.green(),
    )

    for key, val in COMMAND.items():
        alias = val.get("aliases")
        alias = ", ".join(alias) if alias else "[No alias]"
        cmd_desc = f"```{val.get('syntax')}```"
        embed.add_field(name=f"🔸 {key}", value=cmd_desc, inline=False)
    return embed


def _make_command_embed(cmd_name: str) -> Embed:
    value = COMMAND.get(cmd_name)

    aliases = value.get("aliases")
    if aliases:
        aliases = ", ".join(aliases)
    else:
        aliases = "[No alias]"
    title = f"🔶 {cmd_name} (or {aliases})"

    notion_link = value.get("notion_link")

    args_dict = value.get("arguments")
    args_info = (f"\n🔹 {key}\n{val}" for key, val in args_dict.items())
    args_info = "\n".join(args_info)

    cmd_desc = value.get("description")
    examples = "\n".join(value.get("examples"))
    description = f"""\
อ่านคู่มือภาษาไทย [[คลิก]({notion_link})]
🔷 __Description__
{cmd_desc}

```
{value.get("syntax")}
```
Note: "`🧊`" represent one " " (empty space).
🔷 __Arguments info__
{args_info}

🔷 __Example__
```
{examples}
```
"""
    return Embed(title=title, description=description, color=Colour.green())


class HelpCommand(ChemistryCogBase):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="help")
    async def _help(self, ctx: Context, *args: str) -> None:
        if not args:
            await ctx.send(embed=_make_help_embed())
            return
        if args[0] not in COMMAND:
            raise KaitoonValueError(f'Unknown command name "{args[0]}".')
        await ctx.send(embed=_make_command_embed(args[0]))


def setup(bot):
    bot.add_cog(HelpCommand(bot))
