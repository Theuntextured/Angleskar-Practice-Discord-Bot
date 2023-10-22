import botLib


def getHelp(prefix):
    return {
    "help": f"Gives help about commands or a specific command.\n`{prefix}help <(command)>`",
    "setprefix" : f"Sets the new prefix for this bot.\n`{prefix}setprefix <prefix>`",
    "practice" : f"Used in combination to a second command.\nCreate a team with: `{prefix}practice create <weekday> <CET/CEST time in 24h format> <team name>`\nDelete a team with `{prefix}practice delete <practice ID>`",
    "practices": f"Gives all practice sessions on schedule and their index ID.\n`{prefix}practices <(team)>`",
    "team" : f"Used in combination to a second command or gets the info about a team.\nGet team information: `{prefix}team <team>`\nCreate a team: `{prefix}team create <team name> <text channel for reminders> <voice channel>`\nDelete a team: `{prefix}team delete <team>`\nAdd a member to the team: `{prefix}team addmember <team> <user>`\nRemove a member from a team: `{prefix}team removemember <team> <user>`\nAdd a role which will be pinged as reminders to the team: `{prefix}team addrole <team> <role>`\nRemove a role from a team: `{prefix}team removerole <team> <role>`",
    "teams" : f"Gives a list of all teams.\n`{prefix}teams`",
    "permission": f"Gives or removes the permission to edit teams to a role. \n`{prefix}permission <add/remove> <role>`",
    "source": f"Gives the link to the bot's [source code](<https://github.com/Theuntextured/Angleskar-Practice-Discord-Bot/tree/main>).\n`{prefix}source`",
    "roadmap": f"Gives a list of the current [roadmap](<https://trello.com/b/wbeZTFMR/practice-bot>).\n`{prefix}roadmap`"
    }

def handle_response(p_message, botInst, guild, sender) -> str:

    #setup and check prefix
    message = p_message.split()
    message[0] = message[0].lower()
    prefix = botInst.settings["prefix"]
    if (message[0])[0:(len(prefix))] != prefix:
        return
    message[0] = message[0][len(prefix):]

    #setup permission checks
    modPermissions = sender.guild_permissions.moderate_members
    roles = sender.roles
    teamPermissions = False
    for i in roles:
        if i.id in botInst.settings["teamPermRoles"]:
            teamPermissions = True
            break
    teamPermissions = modPermissions or teamPermissions
    
    #help command
    if message[0] == 'help':
        help = getHelp(prefix)
        s = "# __Here is a list of all available commands:__\n\n"
        if len(message) == 1:
            for i in help.keys():
                s += f"## {prefix}{i}\n{help[i]}\n\n"
            return s
        else:
            cmd = message[1].lower()
            if cmd in help.keys():
                return help[cmd]
            else:
                return f"{cmd} is not a recognised command."

    #add/remove team permission roles
    if message[0] == "permission":
        if not modPermissions:
            return "You do not have the permission to use such command."
        if len(message) < 3:
            return "Incorrect usage."
        
        role = guild.get_role(int(message[2][3:len(message[2]) - 1]))

        try:
            roleID = role.id
        except Exception as e:
            return f"\"{message[len(message) - 1]}\" is not a valid role."

        if message[1].lower() == "add":
            if roleID in botInst.settings["teamPermRoles"]:
                return f"{message[len(message) - 1]} already has permissions to use team commands."
            
            botInst.settings["teamPermRoles"].append(roleID)
            botInst.saveSettings()
            return f"{message[len(message) - 1]} now has access to team commands."
        
        if message[1].lower() == "remove":
            if not (roleID in botInst.settings["teamPermRoles"]):
                return f"{message[len(message) - 1]} does not have team commands."
            botInst.settings["teamPermRoles"].remove(roleID)
            botInst.saveSettings()
            return f"{message[len(message) - 1]} now has been revoked of team command permissions."
    
    #source and roadmap
    if message[0] == "source":
        return "[Here](https://github.com/Theuntextured/Angleskar-Practice-Discord-Bot/tree/main) you can find the source code for the bot."
    if message[0] == "roadmap":
        return "[Here](https://trello.com/b/wbeZTFMR/practice-bot) you can find the roadmap for the bot's development."
    
    #practice commands
    if message[0] == "practice":

        if not teamPermissions:
            return "You do not have the permission to use such command."

        if len(message) < 3:
            return "Incorrect usage."
        
        #create a practice
        if message[1] == "create":
            if len(message) < 5:
                return f"Incorrect format. use `{prefix}help createpractice` to view the correct format."
            if botLib.weekdays.count(message[2].capitalize()) == 0:
                return f'"{message[2]}" is not a valid week day.'

            team = botLib.combineToString(message[4:]).lower()

            if not(team in botInst.teams.keys()):
                return f"\"{team}\" is not a valid team."
            if not botLib.isTimeFormat(message[3]):
                return f"\"{message[3]}\" is not a valid time format."
            
            newPractice = {"weekday" : message[2].capitalize(), "time" : message[3], "team" : team}
            botInst.practices.append(newPractice)
            botInst.savePractices()
            return f'Added a practice session which will occur every {newPractice["weekday"]} at {newPractice["time"]} CET for the team {newPractice["team"].title()}.'
        
        #remove practice session
        if message[1] == "delete":
            if len(message) == 2:
                return f"Incorrect format"
            index = int(message[2]) - 1

            if index >= len(botInst.practices) or index < 0:
                return "The index is invalid."
            s = f"Practice session at index {index + 1} hass successfully been deleted."
            botInst.practices.pop(index)
            botInst.savePractices()
            return s

    #practice list
    if message[0] == "practices":
        practices = botInst.practices

        if len(message) > 1:
            team = botLib.combineToString(message[1:]).lower()
            s = ""
            for i in range(0, len(practices)):
                if practices[i]['team'] == team:
                    s = s + "\n" + f"{i + 1}: Practice session every {practices[i]['weekday']} at {practices[i]['time']}."

            return f"**The current practice sessions for {team.title()} are:**\n" + s if len(s) > 0 else f"There are no active practices for {team.title()}."


        s = ""
        for i in range(0, len(practices)):
            s = s + "\n" + f"{i + 1}: {practices[i]['team'].title()} has a practice session every {practices[i]['weekday']} at {practices[i]['time']}."

        return "**The current practice sessions are:**\n" + s if len(s) > 0 else "There are no active practices."
    
    #set prefix
    if message[0] == "setprefix":

        if not modPermissions:
            return "You do not have the permission to use such command."

        if len(message) > 1:
            botInst.settings["prefix"] = message[1]
            botInst.saveSettings()
            return "The new prefix has been set to " + message[1]
        else:
            return f"Usage for the command is `{prefix}setprefix <prefix>"
        
    #team list
    if message[0] == "teams":
        s = ""
        for i in botInst.teams.keys():
            s += "* " + i.title() + "\n"
        
        if s == "":
            return f"There are no teams yet. Use {prefix}createteam to create one."
        else:
            return "**The current teams are:**\n\n" + s
        
    #team commands
    if message[0] == "team":
        if len(message) == 1:
            return f"Incorrect format. Use {prefix}team to view the correct format."
        
        #Add member to team
        if message[1].lower() == "addmember":

            if not teamPermissions:
                return "You do not have the permission to use such command."

            if len(message) == 2:
                return "Please specify what member should be added to the team."

            try:
                user = botInst.client.get_user(int(message[len(message) - 1][2:len(message[len(message) - 1])-1]))
                ID = user.id
            except Exception as e:
                return f"\"{message[len(message) - 1]}\" is not a valid user."
            
            team = ""
            for i in range(2, len(message) - 1):
                team += message[i] + " "
            team = team[0:len(team)-1].lower()

            if not (team in botInst.teams.keys()):
                return f'"{team}" is not a valid team.'

            if ID in botInst.teams[team]["players"]:
                return f"{message[len(message) - 1]} is already a member of {team}."

            botInst.teams[team]["players"].append(ID)
            botInst.saveTeams()
            return f"<@{ID}> is now a member of {team}."
        
        #create team
        if message[1].lower() == "create":

            if not teamPermissions:
                return "You do not have the permission to use such command."

            message[2] = message[2].lower()
            if len(message) < 5:
                return f"Incorrect syntax. Use `{prefix}help team` to view the correct format."
            
            try:
                VCObject = botInst.client.get_channel(int(message[len(message)-1][2:len(message[len(message)-1])-1]))
            except Exception as e:
                return f'"{message[len(message)-1]}" is not a valid voice channel.'
            if (VCObject == None) or (str(VCObject.type) != "voice"):
                return f'"{message[len(message)-1]}" is not a valid voice channel.'
            
            try:
                TCObject = botInst.client.get_channel(int(message[len(message)-2][2:len(message[len(message)-1])-1]))
            except Exception as e:
                return f'"{message[len(message)-2]}" is not a valid text channel.'
            if (TCObject == None) or (str(TCObject.type) != "text"):
                return f'"{message[len(message)-2]}" is not a valid text channel.'
            
            name = ""
            for i in range(2, len(message) - 2):
                name += message[i] + " "
            
            name = name[:len(name)-1]
            
            if name in botInst.teams:
                return f"{name} is already a team."
            
            
            newTeam = {"vc" : message[len(message)-1][2:len(message[len(message)-1])-1], "tc": message[len(message)-2][2:len(message[len(message)-1])-1], "players" : [], "roles" : []}
            botInst.teams[name] = (newTeam)
            botInst.saveTeams()
            return f"{name.title()} has successfully been created."
            
        #add role to team
        if message[1].lower() == "addrole":

            if not teamPermissions:
                return "You do not have the permission to use such command."

            name = ""
            for i in range(2, len(message) - 1):
                name += message[i] + " "
            name = name[:len(name)-1].lower()

            if not (name in botInst.teams.keys()):
                return f"\"{name}\" is not a valid team."
            
            role = guild.get_role(int(message[len(message) - 1][3:len(message[len(message) - 1]) - 1]))

            try:
                roleID = role.id
            except Exception as e:
                return f"\"{message[len(message) - 1]}\" is not a valid role."
            
            if roleID in botInst.teams[name]["roles"]:
                return f"<@&{roleID}> has already been added to the team."
            
            botInst.teams[name]["roles"].append(roleID)
            botInst.saveTeams()
            return f"The role <@&{roleID}> was successfully added to {name.capitalize()}."

        if message[1].lower() == "removerole":

            if not teamPermissions:
                return "You do not have the permission to use such command."
            
            team = botLib.combineToString(message[2:len(message) - 1]).lower()
            if not (team in botInst.teams.keys()):
                return f"{team.title()} is not a valid team."
            roleID = int(message[len(message) - 1][3:len(message[len(message) - 1]) - 1])
            if not (roleID in botInst.teams[team]["roles"]):
                return f"message[len(message) - 1] is not part of {team.title()}."
            botInst.teams[team]["roles"].remove(roleID)
            botInst.saveTeams()
            return f"{message[len(message) - 1]} has been been removed from {team.title()}."

        #delete team
        if message[1].lower() == "delete":

            if not teamPermissions:
                return "You do not have the permission to use such command."

            if len(message) == 2:
                return "Please specify the team to delete."
            
            team = botLib.combineToString(message[2:]).lower()

            if not (team in botInst.teams.keys()):
                return f"{team.title()} is not a valid team."
            
            botInst.teams.pop(team)

            botInst.saveTeams()
            botInst.savePractices()
            return f"{team.title()} has been deleted."

        #remove member from team
        if message[1].lower() == "removemember":

            if not teamPermissions:
                return "You do not have the permission to use such command."
            
            if len(message) == 2:
                return "Please specify the team and the player to remove."
            team = botLib.combineToString(message[2:len(message) - 1]).lower()
            if not (team in botInst.teams.keys()):
                return f"{team.title()} is not a valid team."
            userID = int(message[len(message) - 1][2:len(message[len(message) - 1]) - 1])
            try:
                user = botInst.client.get_user(userID)
                userID = user.id
            except Exception as e:
                return f"\"{message[len(message) - 1]}\" is not a valid user."
            if not(userID in  botInst.teams[team]["players"]):
                return f"{message[len(message) - 1]} is not in {team.title()}."
            botInst.teams[team]["players"].remove(userID)
            botInst.saveTeams()
            return f"{message[len(message) - 1]} has been successfully removed from {team.title()}."

        #team info
        else:
            team = ""
            for i in range(1, len(message)):
                team += message[i] + " "
            team = team[0:len(team)-1].lower()
            if not (team in botInst.teams.keys()):
                return f"{team} is not a valid team."
            s = ""
            for i in botInst.teams[team]["players"]:
                s+= f"* {botInst.client.get_user(int(i)).display_name}\n"
            if s == "":
                s = "The team contains no players."
            else:
                s = f"The current roster for team {team.title()} is:\n\n" + s
            
            roles = ""
            for i in botInst.teams[team]["roles"]:
                roles += f"* {guild.get_role(int(i)).name}\n"
            if roles == "":
                roles = f"There are currently no roles for team {team.title()}.\n"
            else:
                roles = "The current roles assigned to the team are:\n\n" + roles
            
            return f"{team.title()} uses text channel <#{botInst.teams[team]['tc']}> and voice channel <#{botInst.teams[team]['vc']}>.\n\n" + roles + "\n" + s
            