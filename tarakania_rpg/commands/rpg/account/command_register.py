from command import BaseCommand, CommandResult
from argparser.arguments import Arguments
from context import Context

from rpg.player import Player, NickOrIDUsed
from rpg.rpg_object import all_instances, UnknownObject
from rpg.race import Race
from rpg.class_ import Class


class Command(BaseCommand):
    async def run(self, ctx: Context, args: Arguments) -> CommandResult:
        nick = args[0]

        if not (1 <= len(nick) <= 128):
            return f"Имя персонажа должно быть в пределах от **1** до **128** символов.\nВы ввели **{len(nick)}**"

        try:
            race: Race = Race.from_name(args[1])
        except UnknownObject:
            return f"Выберите название расы из: **{', '.join(i.name for i in all_instances(Race))}**"

        try:
            class_: Class = Class.from_name(args[2])
        except UnknownObject:
            return f"Выберите название класса из: **{', '.join(i.name for i in all_instances(Class))}**"

        try:
            await Player.create(
                self.bot.pg, ctx.author.id, nick, race.id, class_.id
            )
        except NickOrIDUsed:
            return "Персонаж с таким именем уже существует или у вас уже есть персонаж"

        return "Персонаж создан"
