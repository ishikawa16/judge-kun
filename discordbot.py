from discord.ext import commands
from os import getenv
import traceback

from manager import Manager

bot = commands.Bot(command_prefix='/')
manager = Manager()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def add(ctx, *args):
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
    if ctx.invoked_subcommand is None:
        await ctx.send('表示するものを以下から指定してください\n{player, ranking, rule}')


@show.command()
async def player(ctx):
    msg = manager.display_players()
    await ctx.send(msg)


@show.command()
async def ranking(ctx):
    msg = manager.display_ranking()
    await ctx.send(msg)


@show.command()
async def rule(ctx):
    msg = manager.display_rule()
    await ctx.send(msg)


@bot.group(name='set')
async def set_(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('以下のいずれかを指定してください\n{team, weapon}')


@set_.group()
async def team(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('チーム分けのルールを以下から指定してください\n{win_percentage, random, fixed}')


@team.command(name='win_percentage')
async def win_percentage_team(ctx):
    manager.set_team_option('-w')
    msg = manager.display_rule()
    await ctx.send(msg)


@team.command(name='random')
async def random_team(ctx):
    manager.set_team_option('-r')
    msg = manager.display_rule()
    await ctx.send(msg)


@team.command(name='fixed')
async def fixed_team(ctx):
    if manager.is_first_battle():
        await ctx.send('前の試合が存在しません')
        return
    manager.set_team_option('-f')
    msg = manager.display_rule()
    await ctx.send(msg)


@set_.group()
async def weapon(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('武器決めのルールを以下から指定してください\n{all, random}')


@weapon.command(name='all')
async def all_weapon(ctx):
    manager.set_weapon_option('-a')
    msg = manager.display_rule()
    await ctx.send(msg)


@weapon.command(name='random')
async def random_weapon(ctx):
    manager.set_weapon_option('-r')
    msg = manager.display_rule()
    await ctx.send(msg)


@bot.command()
async def split(ctx):
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
    if ctx.invoked_subcommand is None:
        await ctx.send('勝利チームを指定してください')


@report.command()
async def alpha(ctx):
    if not manager.is_during_battle():
        await ctx.send('試合開始前です')
        return

    manager.report_alpha_win()
    manager.finish_battle()
    await ctx.send('アルファチームの勝利を記録しました')


@report.command()
async def bravo(ctx):
    if not manager.is_during_battle():
        await ctx.send('試合開始前です')
        return

    manager.report_bravo_win()
    manager.finish_battle()
    await ctx.send('ブラボーチームの勝利を記録しました')


@bot.command()
async def exit(ctx: commands.Context):
    await bot.close()


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
