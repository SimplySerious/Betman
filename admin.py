from discord.ext import commands
import asyncio


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="Load", help="Loads an Extension.")
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        cog = self.client.get_cog(module)
        self.client.add_cog(cog)
        await ctx.send(":thumbsup:")

    @commands.command(name="Unload", help="UnLoads an Extension.")
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        cog = self.client.get_cog(module)
        self.client.remove_cog(cog)
        await ctx.send(":thumbsup:")

    @commands.command(name="Reload", help="Reloads an Extension.")
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        cog = self.client.get_cog(module)
        self.client.remove_cog(cog)
        self.client.add_cog(cog)
        await ctx.send(":thumbsup:")
