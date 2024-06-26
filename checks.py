from typing import Any, Callable, TypeVar

import discord

T = TypeVar("T")


class CheckAnyFailure(discord.app_commands.errors.CheckFailure):
    def __init__(self, exceptions: dict[Callable[..., Any], discord.app_commands.CheckFailure]) -> None:
        self.exceptions: dict[Callable[..., Any], discord.app_commands.CheckFailure] = exceptions
        super().__init__("All checks failed.")


def app_check_any(*checks: Callable[[T], T]):
    def get_predicate(check) -> Callable[[discord.Interaction], bool]:
        fake: Callable[..., None] = lambda _: None
        check(fake)
        checks = fake.__discord_app_commands_checks__
        return checks[0]

    async def predicate(interaction: discord.Interaction) -> bool:
        exceptions: dict[Callable[..., Any], discord.app_commands.CheckFailure] = {}
        for check in checks:
            try:
                return get_predicate(check)(interaction)
            except discord.app_commands.CheckFailure as e:
                exceptions[check] = e

        raise CheckAnyFailure(exceptions)

    return discord.app_commands.check(predicate)