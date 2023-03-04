import traceback

from discord.ext import commands

from manager import Manager


class JudgeCog(commands.Cog, name="プライベートマッチ関連"):
    """ジャッジくんのコマンドを定義
    """
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.manager = Manager()

    @commands.command()
    async def add(self, ctx, *args):
        """プレイヤーの追加
        """
        if len(args) == 0:
            msg = "名前を指定してください"
            await ctx.send(msg)
            return

        for name in sorted(set(args), key=args.index):
            if not self.manager.has_player(name):
                self.manager.add_player(name)

        msg = self.manager.display_players()
        await ctx.send(msg)

    @commands.command()
    async def change(self, ctx, *args):
        """プレイヤーの武器変更
        """
        if len(args) == 0:
            msg = "名前を指定してください"
            await ctx.send(msg)
            return

        battle = self.manager.get_battle()
        rule = self.manager.get_rule()
        weapon_option = rule.get_weapon_option()
        if not battle.is_prepared() or weapon_option != "-r":
            msg = "武器が指定されていません"
            await ctx.send(msg)
            return

        for name in sorted(set(args), key=args.index):
            if battle.has_player(name):
                battle.change_weapon(name)

        msg = self.manager.display_teams()
        await ctx.send(msg)

    @commands.command()
    async def delete(self, ctx, *args):
        """プレイヤーの削除
        """
        if len(args) == 0:
            msg = "名前を指定してください"
            await ctx.send(msg)
            return

        for name in sorted(set(args), key=args.index):
            if self.manager.has_player(name):
                self.manager.remove_player(name)

        msg = self.manager.display_players()
        await ctx.send(msg)

    @commands.group()
    async def report(self, ctx):
        """試合の勝利報告
        """
        if ctx.invoked_subcommand is None:
            msg = "勝利チームを指定してください"
            await ctx.send(msg)

    @report.command(name="1")
    async def team1(self, ctx):
        """チーム1の勝利報告
        """
        battle = self.manager.get_battle()
        if not battle.is_prepared():
            msg = "試合開始前です"
            await ctx.send(msg)
            return

        self.manager.record_battle(1)
        msg = "チーム1の勝利を記録しました"
        await ctx.send(msg)

    @report.command(name="2")
    async def bravo(self, ctx):
        """チーム2の勝利報告
        """
        battle = self.manager.get_battle()
        if not battle.is_prepared():
            msg = "試合開始前です"
            await ctx.send(msg)
            return

        self.manager.record_battle(2)
        msg = "チーム2の勝利を記録しました"
        await ctx.send(msg)

    @commands.command()
    async def reset(self, ctx):
        """記録のリセット
        """
        del self.manager
        self.manager = Manager()
        msg = "記録した情報を全てリセットしました"
        await ctx.send(msg)

    @commands.group()
    async def set(self, ctx):
        """ルールの設定/変更
        """
        if ctx.invoked_subcommand is None:
            msg = ("以下のいずれかを指定してください"
                   "{t(team), w(weapon)}")
            await ctx.send(msg)

    @set.group(name="t")
    async def team(self, ctx):
        """チームに関するルール設定/変更
        """
        if ctx.invoked_subcommand is None:
            msg = ("チーム分けのルールを以下から指定してください\n"
                   "{w(ranking), r(random), f(fixed)}")
            await ctx.send(msg)

    @team.command(name="w")
    async def ranking_team(self, ctx):
        """チーム -> 勝率
        """
        rule = self.manager.get_rule()
        rule.set_team_option("-w")
        msg = rule.display()
        await ctx.send(msg)

    @team.command(name="r")
    async def random_team(self, ctx):
        """チーム -> ランダム
        """
        rule = self.manager.get_rule()
        rule.set_team_option("-r")
        msg = rule.display()
        await ctx.send(msg)

    @team.command(name="f")
    async def fixed_team(self, ctx):
        """チーム -> 固定
        """
        battle = self.manager.get_latest_battle()
        if battle is None:
            msg = "前の試合が存在しません"
            await ctx.send(msg)
            return

        rule = self.manager.get_rule()
        rule.set_team_option("-f")
        msg = rule.display()
        await ctx.send(msg)

    @set.group(name="w")
    async def weapon(self, ctx):
        """武器に関するルール設定/変更
        """
        if ctx.invoked_subcommand is None:
            msg = ("武器決めのルールを以下から指定してください\n"
                   "{a(all), r(random)}")
            await ctx.send(msg)

    @weapon.command(name="a")
    async def all_weapon(self, ctx):
        """武器 -> 指定なし
        """
        rule = self.manager.get_rule()
        rule.set_weapon_option("-a")
        msg = rule.display()
        await ctx.send(msg)

    @weapon.command(name="r")
    async def random_weapon(self, ctx):
        """武器 -> ランダム
        """
        rule = self.manager.get_rule()
        rule.set_weapon_option("-r")
        msg = rule.display()
        await ctx.send(msg)

    @commands.group()
    async def show(self, ctx):
        """プレイヤー/ルールの表示
        """
        if ctx.invoked_subcommand is None:
            msg = ("表示するものを以下から指定してください\n"
                   "{p(player), w(ranking), r(rule)}")
            await ctx.send(msg)

    @show.command(name="p")
    async def player(self, ctx):
        """プレイヤーの一覧表示
        """
        msg = self.manager.display_players()
        await ctx.send(msg)

    @show.command(name="w")
    async def ranking(self, ctx):
        """プレイヤーの勝率表示
        """
        msg = self.manager.display_ranking()
        await ctx.send(msg)

    @show.command(name="r")
    async def rule(self, ctx):
        """ルールの表示
        """
        rule = self.manager.get_rule()
        msg = rule.display()
        await ctx.send(msg)

    @commands.command()
    async def split(self, ctx):
        """試合のチーム分け
        """
        if self.manager.is_short():
            msg = "プレイヤーの人数が不足しています"
            await ctx.send(msg)
            return

        if self.manager.is_over():
            msg = "プレイヤーの人数が制限を超えています"
            await ctx.send(msg)
            return

        rule = self.manager.get_rule()
        if not rule.is_determined():
            msg = "ルールを指定してください"
            await ctx.send(msg)
            return

        is_success = self.manager.prepare_battle()

        if is_success:
            msg = self.manager.display_teams()
        else:
            msg = "チーム分けに失敗しました"
        await ctx.send(msg)

    @commands.command()
    async def switch(self, ctx, *args):
        """プレイヤーの状態切り替え
        """
        if len(args) == 0:
            msg = "名前を指定してください"
            await ctx.send(msg)
            return

        for name in sorted(set(args), key=args.index):
            if self.manager.has_player(name):
                player = self.manager.get_player(name)
                player.change_status()

        msg = self.manager.display_players()
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """コマンドのエラー処理
        """
        if isinstance(error, commands.errors.CommandNotFound):
            error_msg = "存在しないコマンドです"
        else:
            orig_error = getattr(error, "original", error)
            error_msg = "".join(traceback.TracebackException.from_exception(orig_error).format())
        await ctx.send(error_msg)


async def setup(bot):
    await bot.add_cog(JudgeCog(bot))
