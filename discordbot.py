import discord
from discord.ext import commands
import os
import traceback

# @commands.event
# async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)


# classにまとめます
class thanatos_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        # カテゴリ関係
        # 本当はclassにまとめた方がきっときれいだが、面倒なので順序を保ったリストをzipでまとめる
        # entry用
        self.keys = ["tank", "saint", "dark", "am", "rm", "lb", "dram", "sora", "luna", "other", "free", "absent", "earlybird", "nightowl"]
        self.marks = ['🛡️', '💚', '💜', '✨', '⚔', '🤖', '🐱', '☀', '🌙', '🔥', '🆓', '💤', '🐔', '🦉']
        self.labels = ["タンク", "支援セイント", "闇変セイント", "アーケインマスター", "ルーンマスター", "ライトブリンガー", "ドラム", "ソラリス",
                  "ルナリス", "その他火力", "フリー参加", "欠席", "早め希望", "遅め希望"]
        # organize用
        self.pt_keys = ["salt", "non-salt"]
        self.pt_marks = ['🈶', '🈚']
        self.pt_labels = ["塩PT", "無塩PT"]
        
        # organize_future用
        self.pt_future_keys = ["maintank", "subtank", "saint", "dark", "am", "rm", "lb", "dram", "lunasora", "other"]
        self.pt_future_marks = ['🛡️', '🛡️', '💚', '💜', '✨', '⚔', '🤖', '🐱', '☀', '🔥']
        self.pt_future_labels = ["メインタンク", "サブタンク", "支援セイント", "闇変セイント", "アーケインマスター", "ルーンマスター", "ライトブリンガー", 
                                 "ドラム", "ルナソラ", "その他火力"]

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def _update_reactions(self, payload, pt_mode=False):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        embed = msg.embeds[0]
        # add/removeが発生したリアクションのリストを更新する
        label = "\u200b"
        if pt_mode:
            id = self.pt_marks.index(payload.emoji.name)
            name = self.pt_marks[id] + self.pt_labels[id]
        else:
            id = self.marks.index(payload.emoji.name)
            name = self.marks[id] + self.labels[id]
        users = await msg.reactions[id].users().flatten()
        for u in users:
            # botでないユーザの名前を改行挟んで文字列連結
            # 本当は上のリストをうまく絞り込んでjoinするのがpythonっぽいはずだがスキル不足である
            if not u.bot:
                label += u.name + '\n'
        embed.set_field_at(id, name=name, value=label, inline=True)
        await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.member.bot:
            if payload.emoji.name in self.marks:
                await self._update_reactions(payload)
            elif payload.emoji.name in self.pt_marks:
                await self._update_reactions(payload, pt_mode=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name in self.marks:
            await self._update_reactions(payload)
        elif payload.emoji.name in self.pt_marks:
            await self._update_reactions(payload, pt_mode=True)

    @commands.command()
    async def entry_hero(self, ctx, date=""):
        # 最初の描画
        embed = discord.Embed()
        embed.title = f"タナトスヒーロー エントリー ： {date} "
        for key, mark, label in zip(self.keys, self.marks, self.labels):
            embed.add_field(name=mark+label, value="\u200b", inline=True)
        msg = await ctx.send(embed=embed)
        for mark in self.marks:
            await msg.add_reaction(mark)

    @commands.command()
    async def organize_hero(self, ctx, datetime):
        embed = discord.Embed()
        embed.title = f"タナトスヒーロー パーティ編成： {datetime}"
        for key, mark, label in zip(self.pt_keys, self.pt_marks, self.pt_labels):
            embed.add_field(name=mark+label, value="\u200b", inline=True)
        msg = await ctx.send(embed=embed)
        for mark in self.pt_marks:
            await msg.add_reaction(mark)

    @commands.command()
    async def organize_future_hero(self, ctx, datetime, pttype):
        embed = discord.Embed()
        embed.title = f"タナトスヒーロー パーティ編成： {datetime} {pttype}"
        for key, mark, label in zip(self.pt_future_keys, self.pt_future_marks, self.pt_future_labels):
            embed.add_field(name=mark+label, value="\u200b", inline=True)
        msg = await ctx.send(embed=embed)
        for mark in self.pt_future_marks:
            await msg.add_reaction(mark)
            
if __name__ == '__main__':
    bot = commands.Bot(command_prefix='/')  # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.add_cog(thanatos_Cog(bot))
    token = os.environ['DISCORD_BOT_TOKEN']
    bot.run(token)
