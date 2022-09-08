from discord.ext import commands


class JapaneseHelpCommand(commands.DefaultHelpCommand):
    """helpコマンドの表示内容を日本語化
    """
    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix
        self.no_category = "基本コマンド"
        self.command_attrs["help"] = "各コマンドの説明を表示"

    def get_ending_note(self):
        return (f"各コマンドの説明: {self.prefix}help <コマンド名>\n"
                f"各カテゴリの説明: {self.prefix}help <カテゴリ名>\n")
