import traceback

from discord.ext import commands

from manager import Manager


class JudgeCog(commands.Cog):
    """ジャッジくんのコマンドを定義
    """
    def __init__(self, bot):
        self.bot = bot
        self.manager = Manager()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """コマンドのエラー処理
        """
        orig_error = getattr(error, "original", error)
        error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        await ctx.send(error_msg)

    @commands.command()
    async def add(self, ctx, *args):
        """プレイヤーの追加
        """
        if self.manager.is_during_battle():
            await ctx.send('試合が終了するまでプレイヤーの登録はできません')
            return

        if len(args) == 0:
            await ctx.send('名前を指定してください')
            return

        for name in args:
            if not self.manager.has_player(name):
                self.manager.add_player(name)

        msg = self.manager.display_players()
        await ctx.send(msg)

    @commands.command()
    async def delete(self, ctx, *args):
        """プレイヤーの削除
        """
        if self.manager.is_during_battle():
            await ctx.send('試合が終了するまでプレイヤーの削除はできません')
            return

        if len(args) == 0:
            await ctx.send('名前を指定してください')
            return

        for name in args:
            if self.manager.has_player(name):
                self.manager.remove_player(name)

        msg = self.manager.display_players()
        await ctx.send(msg)

    @commands.group()
    async def show(self, ctx):
        """プレイヤー/ルールの表示
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('表示するものを以下から指定してください\n{p(player), w(ranking), r(rule)}')

    @show.command(name='p')
    async def player(self, ctx):
        """プレイヤーの一覧表示
        """
        msg = self.manager.display_players()
        await ctx.send(msg)

    @show.command(name='w')
    async def ranking(self, ctx):
        """プレイヤーの勝率表示
        """
        msg = self.manager.display_ranking()
        await ctx.send(msg)

    @show.command(name='r')
    async def rule(self, ctx):
        """ルールの表示
        """
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @commands.group()
    async def set(self, ctx):
        """ルールの設定/変更
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('以下のいずれかを指定してください\n{t(team), w(weapon)}')

    @set.group(name='t')
    async def team(self, ctx):
        """チームに関するルール設定/変更
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('チーム分けのルールを以下から指定してください\n{w(ranking), r(random), f(fixed)}')

    @team.command(name='w')
    async def ranking_team(self, ctx):
        """チーム -> 勝率
        """
        self.manager.set_team_option('-w')
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @team.command(name='r')
    async def random_team(self, ctx):
        """チーム -> ランダム
        """
        self.manager.set_team_option('-r')
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @team.command(name='f')
    async def fixed_team(self, ctx):
        """チーム -> 固定
        """
        if self.manager.is_first_battle():
            await ctx.send('前の試合が存在しません')
            return
        self.manager.set_team_option('-f')
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @set.group(name='w')
    async def weapon(self, ctx):
        """武器に関するルール設定/変更
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('武器決めのルールを以下から指定してください\n{a(all), r(random)}')

    @weapon.command(name='a')
    async def all_weapon(self, ctx):
        """武器 -> 指定なし
        """
        self.manager.set_weapon_option('-a')
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @weapon.command(name='r')
    async def random_weapon(self, ctx):
        """武器 -> ランダム
        """
        self.manager.set_weapon_option('-r')
        msg = self.manager.display_rule()
        await ctx.send(msg)

    @commands.command()
    async def split(self, ctx):
        """試合のチーム分け
        """
        if self.manager.is_short():
            await ctx.send('プレイヤーの人数が不足しています')
            return

        if self.manager.is_over():
            await ctx.send('プレイヤーの人数が制限を超えています')
            return

        if not self.manager.rule_determined():
            await ctx.send('ルールを指定してください')
            return

        self.manager.split_players()
        self.manager.specify_weapons()
        self.manager.start_battle()

        msg = self.manager.display_teams()
        await ctx.send(msg)

    @commands.command()
    async def change(self, ctx, *args):
        """プレイヤーの武器変更
        """
        if not self.manager.is_during_battle() or not self.manager.weapon_specified():
            await ctx.send('武器が指定されていません')
            return

        if len(args) == 0:
            await ctx.send('名前を指定してください')
            return

        self.manager.change_weapons(args)
        msg = self.manager.display_teams()
        await ctx.send(msg)

    @commands.group()
    async def report(self, ctx):
        """試合の勝利報告
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('勝利チームを指定してください')

    @report.command(name='a')
    async def alpha(self, ctx):
        """アルファチームの勝利報告
        """
        if not self.manager.is_during_battle():
            await ctx.send('試合開始前です')
            return

        self.manager.report_alpha_win()
        self.manager.finish_battle()
        await ctx.send('アルファチームの勝利を記録しました')

    @report.command(name='b')
    async def bravo(self, ctx):
        """ブラボーチームの勝利報告
        """
        if not self.manager.is_during_battle():
            await ctx.send('試合開始前です')
            return

        self.manager.report_bravo_win()
        self.manager.finish_battle()
        await ctx.send('ブラボーチームの勝利を記録しました')


async def setup(bot):
    await bot.add_cog(JudgeCog(bot))
