import discord
from discord import Game

TOKEN = '<Your TOKEN here!>'
KICK_ROLE = 'besucher'
INVITE_ROLE = 'test'
NACHRICHT_ROLE = 'test'
CHANNEL_NAME = 'bot'
VOICE_CHANNEL = 'Voice'
#you need to put the file location here for the bot to include it in your message
BILD = '<path to file>'

client = discord.Client()


def bot_channel(channel_name, message):
    if message.channel.name == channel_name:
        return True
    else:
        return False


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if bot_channel(CHANNEL_NAME, message):
        if message.author == client.user:
            return

        if message.content.startswith('!switch_role'):
            content = message.content.split('+')
            if len(content) is 3:
                old_role, new_role = content[1], content[2]

                #members = message.server.members
                members = message.server.members
                member_list = []
                for member in members:
                    member_list.append(member)
                for member in member_list:
                    role_list = get_roles(member)

                    role_to_add = discord.utils.get(member.server.roles, name=new_role)
                    if role_to_add == None:
                        print('Die Rolle konnte nicht vergeben werden: " ' + new_role, '" Bitte Schreibweise überprüfen')
                        break

                    role_to_remove = discord.utils.get(member.server.roles, name=old_role)
                    if role_to_remove == None:
                        print('Die Rolle konnte nicht entfernt werden: " ' + old_role, '" Bitte Schreibweise überprüfen')
                        break

                    if old_role in role_list and client.user != member:
                        await client.add_roles(member, role_to_add)
                        print('"{}" bekam Rolle "{}"'.format(member.name, role_to_add))
                        await client.remove_roles(member, role_to_remove)
                        print('"{}" verlor Rolle "{}"'.format(member.name, role_to_remove))
                    #this is for the @everyone role
                    #if len(role_list) == 1:
                        #await client.add_roles(member, role_to_add)
                        #print("{} wurde zu {}".format(member.name,role_to_add))


        if message.content.startswith('!give_role'):
            content = message.content.split('+')
            if len(content) is 2:
                new_role = content[1]

                members = message.server.members
                member_list = []
                for member in members:
                    member_list.append(member)
                for member in member_list:
                    role_to_add = discord.utils.get(member.server.roles, name=new_role)
                    if role_to_add == None:
                        print('Die Rolle konnte nicht vergeben werden: " ' + new_role, '" Bitte Schreibweise überprüfen')
                    elif client.user != member:
                        await client.add_roles(member, role_to_add)
                        print('User "{}" bekam Rolle "{}"'.format(member.name, role_to_add.name))


        if message.content.startswith('!kick'):
            kick_list = []
            members = message.server.members
            for member in members:
                role_list = get_roles(member)
                if len(role_list) is 1:
                    #new_role = discord.utils.get(message.server.roles, name='besucher')
                    #await client.add_roles(member, new_role)
                    kick_list.append(member)
            for n in kick_list:
                await client.kick(n)

        if message.content.startswith('!invite'):
            content = message.content.split('+')

            if len(content) is 3:
                link, text = content[1], content[2]
                if link.startswith('https://discord.gg/'):  # https://discord.gg/
                    members = message.server.members
                    member_list = []
                    for member in members:
                        member_list.append(member)
                    for member in member_list:
                        role_list = get_roles(member)
                        for role in role_list:
                            if role == INVITE_ROLE:
                                msg = 'Hallo {0.name}\n' \
                                      '{1}\n'\
                                      '{2}'.format(member, text, link)
                                #print(member.name)
                                try:
                                    await client.send_message(member, msg)
                                    check = "erfolgreich"
                                except:
                                    check = "gescheitert"
                                    # print("{} hat Direktnachrichten geblockt".format(member.name))
                                print(member.name, check)
                else:
                    msg = 'Hello {0.author.mention}, the Invite link seems invalid!\n' \
                          'This is what i got from you: `{1}`'.format(message, link)
                    await client.send_message(message.channel, msg)
            else:
                msg = 'Hallo {0.author.mention}, something went wrong\n ' \
                      'the correct format is `"!invite+YOUR_INVITE_LINK_HERE+EVENT_INFO"`?\n' \
                      '`!invite` is what gets my attention\n' \
                      '`+` is how i know what the link and what the Event info is\n' \
                      'I need all 3 (!Invite, the link and the event info)separated with `+`\n' \
                      'You can and should include a time and date in the event info but do NOT use `+` or i will get confused'.format(message)
                await client.send_message(message.channel, msg)

        if message.content.startswith('!nachricht'):
            content = message.content.split('+')

            if len(content) is 3:
                text, n = content[1], content[2]
                members = message.server.members

                #members = message.server.members
                member_list = []
                for member in members:
                    member_list.append(member)
                print(len(member_list))
                for member in member_list:
                    role_list = get_roles(member)
                    for role in role_list:
                        if role == NACHRICHT_ROLE:
                            if n == 't':
                                try:
                                    await client.send_message(member, text)
                                    #await client.send_file(member, BILD)
                                    check = 'erfolgreich'
                                except:
                                    # print("{} hat Direktnachrichten geblockt".format(member.name))
                                    check = 'gescheitert'
                                print(member.name, check)
                            else:
                                try:
                                    #await client.send_file(member, BILD)
                                    await client.send_message(member, text)
                                    check = 'erfolgreich'
                                except:
                                    check = 'gescheitert'
                                print(member.name, check)
                print("fertig")


def get_roles(member: discord.Member):
    """Lists a User's Roles"""
    role_list = []
    for role in member.roles:
        role_list.append(str(role))
    return role_list


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=Game(name='Lieber Gott.'))


client.run(TOKEN)


