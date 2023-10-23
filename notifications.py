import asyncio
import datetime
import botLib
import arrow

#b
b = 0

def getWeekday(t):
    i = 0
    for w in botLib.weekdays:
        if w == t:
            return i
        i += 1

async def handleNotifications(self):

    while True: #loops forever
        n = datetime.datetime.now()

        for p in self.practices:
            team = self.teams[p["team"]]
            target = getWeekday(p["weekday"]) * 24 * 60 + int(p["time"][:len(p["time"]) - 3]) * 60 + int(p["time"][len(p["time"]) - 2:])
            
            if n.weekday() * 24 * 60 + int(n.hour) * 60 + int(n.minute) == target:
                pings = ""
                for i in team["roles"]:
                    pings += f"<@&{i}> "
                vc = f"<#{team['vc']}>"
                text = f"{pings}Join {vc} now! Time for team practice!"
                await self.client.get_channel(int(self.teams[p["team"]]['tc'])).send(text)
            elif n.weekday() * 24 * 60 + int(n.hour) * 60 + int(n.minute) + 30  == target:
                pings = ""
                for i in team["roles"]:
                    pings += f"<@&{i}> "
                vc = f"<#{team['vc']}>"
                text = f"{pings} Remember about practice ! Join {vc} <t:{arrow.get(datetime.datetime.utcnow()).int_timestamp + 30 * 60}:R>"
                await self.client.get_channel(int(self.teams[p["team"]]['tc'])).send(text)
            elif (n.weekday() + 8) % 7 * 24 * 60 + int(n.hour) * 60 + int(n.minute)  == target:
                pings = ""
                for i in team["roles"]:
                    pings += f"<@&{i}> "
                text = f"{pings} Remember about practice <t:{arrow.get(datetime.datetime.utcnow()).int_timestamp + 24 *60 * 60}:R> at <t:{arrow.get(datetime.datetime.utcnow()).int_timestamp + 24 *60 * 60}:t>! React to this message if you can be there!"
                await self.client.get_channel(int(self.teams[p["team"]]['tc'])).send(text)

        await asyncio.sleep(60)