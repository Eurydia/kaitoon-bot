# -*- coding: utf-8 -*-
from discord.ext.commands import command, Context
from discord import Colour, Embed

from timeit import default_timer
from random import randint

from chemistry.cogs.cogs_base import ChemistryCogBase


class BakeACake(ChemistryCogBase):
    @command(name="cake")
    async def bake_a_cake(self, ctx: Context) -> None:
        timer_start = default_timer()
        embed = Embed(title="Baked you a cake.", color=Colour.from_rgb(255, 119, 188))
        embed.add_field(
            name=f"{randint(1, 8)}🌾 + {randint(2, 6)}🥚 + {randint(2, 10)}🍫 = {randint(2,4)}🎂",
            value="Orignal: ```Cake```",
            inline=False,
        )
        embed.add_field(name="Status", value=f"✅ Success (100.0%)", inline=False)
        embed.add_field(name="Inputs", value='🔹 " cake "', inline=False)
        embed.add_field(name="Interpreted as", value='🔸 " 🎂 "', inline=False)
        timer_end = default_timer()
        embed.add_field(
            name="Finished in", value=f"{timer_end-timer_start:.2f}s", inline=False
        )
        await ctx.message.add_reaction("🥳")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BakeACake(bot))
