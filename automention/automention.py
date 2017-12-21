class StupidPeople:
    def __init__(self, bot):
        self.bot = bot
        self.members = {}
        self.updates = {}

    def updated_memberlist(self, server):
        """kek"""
        self.updates[server.id] = self.updates.get(server.id, 0) - 1
        if self.updates[server.id] > 0:
            return self.members[server.id]
        members = {}
        for m in server.members:
            if len(m.name) > 2:
                members.setdefault(m.name, set()).add(m)
            if len(m.display_name) > 2:
                members.setdefault(m.display_name, set()).add(m)
        self.members[server.id] = members
        self.updates[server.id] = 100
        return members


    async def on_message(self, message):
        """snek"""
        if message.author.bot:
            return

        server = message.server
        mlist = self.updated_memberlist(server)

        mentioned = {n: m for n, m in mlist.items() if n in message.content.split()}

        if not mentioned:
            return

        multiple = any(m for m in mentioned.values() if len(m) > 1)

        msg = ("{} Please look at your keyboard and press the @ key before the "
               "person's name to select it.. ".format(message.author.mention))

        if not multiple:
            mentions = []
            for m in mentioned.values():
                mentions.extend(m)
            msg += ("That's what's called a \"**mention\". It looks like this: {}"
                    .format(" ".join(m.mention for m in mentions)))

        await self.bot.send_message(message.channel, msg)

def setup(bot):
    n = StupidPeople(bot)
    bot.add_cog(n)