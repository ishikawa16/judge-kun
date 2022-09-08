from discord.ext import commands
from os import getenv
import traceback

from manager import Manager

bot = commands.Bot(command_prefix='/')
manager = Manager()


@bot.event
async def on_command_error(ctx, error):
    """コマンドのエラー処理
    """
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def add(ctx, *args):
    """プレイヤーの追加
    """
    if manager.is_during_battle():
        await ctx.send('試合が終了するまでプレイヤーの登録はできません')
        return

    if len(args) == 0:
        await ctx.send('名前を指定してください')
        return

    for name in args:
        if not manager.has_player(name):
            manager.add_player(name)

    msg = manager.display_players()
    await ctx.send(msg)


@bot.command()
async def delete(ctx, *args):
    """プレイヤーの削除
    """
    if manager.is_during_battle():
        await ctx.send('試合が終了するまでプレイヤーの削除はできません')
        return

    if len(args) == 0:
        await ctx.send('名前を指定してください')
        return

    for name in args:
        if manager.has_player(name):
            manager.remove_player(name)

    msg = manager.display_players()
    await ctx.send(msg)


@bot.group()
async def show(ctx):
    """プレイヤー/ルールの表示
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('表示するものを以下から指定してください\n{p(player), w(ranking), r(rule)}')


@show.command(name='p')
async def player(ctx):
    """プレイヤーの一覧表示
    """
    msg = manager.display_players()
    await ctx.send(msg)


@show.command(name='w')
async def ranking(ctx):
    """プレイヤーの勝率表示
    """
    msg = manager.display_ranking()
    await ctx.send(msg)


@show.command(name='r')
async def rule(ctx):
    """ルールの表示
    """
    msg = manager.display_rule()
    await ctx.send(msg)


@bot.group()
async def set(ctx):
    """ルールの設定/変更
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('以下のいずれかを指定してください\n{t(team), w(weapon)}')


@set.group(name='t')
async def team(ctx):
    """チームに関するルール設定/変更
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('チーム分けのルールを以下から指定してください\n{w(ranking), r(random), f(fixed)}')


@team.command(name='w')
async def ranking_team(ctx):
    """チーム -> 勝率
    """
    manager.set_team_option('-w')
    msg = manager.display_rule()
    await ctx.send(msg)


@team.command(name='r')
async def random_team(ctx):
    """チーム -> ランダム
    """
    manager.set_team_option('-r')
    msg = manager.display_rule()
    await ctx.send(msg)


@team.command(name='f')
async def fixed_team(ctx):
    """チーム -> 固定
    """
    if manager.is_first_battle():
        await ctx.send('前の試合が存在しません')
        return
    manager.set_team_option('-f')
    msg = manager.display_rule()
    await ctx.send(msg)


@set.group(name='w')
async def weapon(ctx):
    """武器に関するルール設定/変更
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('武器決めのルールを以下から指定してください\n{a(all), r(random)}')


@weapon.command(name='a')
async def all_weapon(ctx):
    """武器 -> 指定なし
    """
    manager.set_weapon_option('-a')
    msg = manager.display_rule()
    await ctx.send(msg)


@weapon.command(name='r')
async def random_weapon(ctx):
    """武器 -> ランダム
    """
    manager.set_weapon_option('-r')
    msg = manager.display_rule()
    await ctx.send(msg)


@bot.command()
async def split(ctx):
    """試合のチーム分け
    """
    if manager.is_short():
        await ctx.send('プレイヤーの人数が不足しています')
        return

    if manager.is_over():
        await ctx.send('プレイヤーの人数が制限を超えています')
        return

    if not manager.rule_determined():
        await ctx.send('ルールを指定してください')
        return

    manager.split_players()
    manager.specify_weapons()
    manager.start_battle()

    msg = manager.display_teams()
    await ctx.send(msg)


@bot.command()
async def change(ctx, *args):
    """プレイヤーの武器変更
    """
    if not manager.is_during_battle() or not manager.weapon_specified():
        await ctx.send('武器が指定されていません')
        return

    if len(args) == 0:
        await ctx.send('名前を指定してください')
        return

    manager.change_weapons(args)
    msg = manager.display_teams()
    await ctx.send(msg)


@bot.group()
async def report(ctx):
    """試合の勝利報告
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('勝利チームを指定してください')


@report.command(name='a')
async def alpha(ctx):
    """アルファチームの勝利報告
    """
    if not manager.is_during_battle():
        await ctx.send('試合開始前です')
        return

    manager.report_alpha_win()
    manager.finish_battle()
    await ctx.send('アルファチームの勝利を記録しました')


@report.command(name='b')
async def bravo(ctx):
    """ブラボーチームの勝利報告
    """
    if not manager.is_during_battle():
        await ctx.send('試合開始前です')
        return

    manager.report_bravo_win()
    manager.finish_battle()
    await ctx.send('ブラボーチームの勝利を記録しました')


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
