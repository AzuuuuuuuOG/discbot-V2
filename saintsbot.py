import discord
from discord.ext import commands, tasks
import datetime
from collections import defaultdict
import json
import uuid
import secrets
import string
import os
import asyncio



intents = discord.Intents.default()
intents.message_content = True  # Tillad læsning og svar på beskeder
intents.reactions = True  # Tillad brug af reaktioner
bot = commands.Bot(command_prefix='!', intents=intents)





# Indlæs data fra JSON-fil, hvis den findes
def load_data1():
    try:
        with open('betalte_personer.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Ingen tidligere data fundet.")
        return []

# Gem data til JSON-fil
def save_data1():
    with open('betalte_personer.json', 'w') as file:
        json.dump(betalte_personer, file)



# Opret en tom liste til at gemme personer, der har betalt
betalte_personer = []


import discord
from discord.ext import commands
import json




betalte_personer = load_data1()  # Indlæs data ved opstart

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

@bot.command()
async def betalt(ctx, person):
    global betalte_personer
    try:
        # Tilføj personen til listen over betalte personer
        betalte_personer.append(person)
        message = await ctx.send(f'{person} har betalt sit kontingent!')
    except Exception as e:
        print(f'Fejl: {e}')
    finally:
        try:
            # Slet beskeden efter 5 sekunder
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
        except discord.errors.NotFound:
            print("Beskeden kunne ikke findes eller er allerede blevet slettet.")
        except Exception as e:
            print(f'Fejl ved sletning af besked: {e}')
        # Gem data
        save_data1()

@bot.command()
async def status(ctx):
    global betalte_personer
    try:
        # Opret en embed-besked til at vise status
        embed = discord.Embed(title="Status for kontingentbetaling", color=discord.Color.purple())  # Blå farve
        if betalte_personer:
            status_besked = "Følgende personer har betalt deres kontingent:\n"
            for person in betalte_personer:
                status_besked += f"- {person}\n"
            embed.description = status_besked
        else:
            embed.description = "Ingen personer har betalt deres kontingent endnu."
        
        # Send embed-beskeden
        await ctx.send(embed=embed)
    except Exception as e:
        print(f'Fejl: {e}')
    finally:
        # Slet kommandobeskeden
        await ctx.message.delete()

@bot.command()
async def nulstil(ctx):
    global betalte_personer
    try:
        betalte_personer = []
        # Send beskeden og gem dens reference
        message = await ctx.send("Betalingsstatus er nulstillet!")
        # Slet begge beskeder efter 5 sekunder
        await asyncio.sleep(5)
        await ctx.message.delete()  # Slet din kommandobesked
        await message.delete()      # Slet botten besked
        # Gem data
        save_data1()
    except discord.errors.NotFound:
        print("Beskeden kunne ikke findes eller er allerede blevet slettet.")
    except Exception as e:
        print(f'Fejl ved sletning af besked: {e}')
        
@bot.command()
async def fjernbetaling(ctx, person):
    global betalte_personer
    try:
        # Fjern personen fra listen over betalte personer
        if person in betalte_personer:
            betalte_personer.remove(person)
            message = await ctx.send(f'{person} er fjernet fra listen over betalte personer.')
        else:
            message = await ctx.send(f'{person} blev ikke fundet på listen over betalte personer.')
    except Exception as e:
        print(f'Fejl: {e}')
    finally:
        try:
            # Slet begge beskeder efter 5 sekunder
            await asyncio.sleep(5)
            await ctx.message.delete()  # Slet din kommandobesked
            await message.delete()      # Slet botten besked
            # Gem data
            save_data1()
        except discord.errors.NotFound:
            print("Beskeden kunne ikke findes eller er allerede blevet slettet.")
        except Exception as e:
            print(f'Fejl ved sletning af besked: {e}')


# Rolle-IDs
rolle_id_1 = 1210069139536879626  # Erstat med den faktiske rolle-ID
rolle_id_2 = 1209253285697945690  # Erstat med den faktiske rolle-ID

# Kanal-ID'er
salg_kanal_id = 1209253134547943494  # Erstat med den faktiske kanal-ID for salg
lab_kanal_id = 1209256295345950750   # Erstat med den faktiske kanal-ID for lab
opgave_kanal_id = 1209253043225370654   # Erstat med den faktiske kanal-ID for opgaver
DONE_CHANNEL_ID = 1209499166502428672  # Erstat med den faktiske kanal-ID, hvor du vil have beskeden skal sendes

JSON_FILE_PATH1 = 'unikke_ids.json'
JSON_FILE_PATH4 = 'opgave_data.json'

def gem_data(data):
    with open(JSON_FILE_PATH1, 'w') as file:
        json.dump(data, file)

# Funktion til at indlæse data fra JSON-fil
def indlæs_data():
    try:
        with open(JSON_FILE_PATH1, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def generate_unique_id():
    while True:
        unique_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        if unique_id not in unikke_ids:
            return unique_id

unikke_ids = indlæs_data()


@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

@bot.event
async def on_reaction_add(reaction, user):
    timestamp = reaction.message.created_at
    if str(reaction.emoji) == '✅' and reaction.message.channel.id in [salg_kanal_id, lab_kanal_id]:
        guild = reaction.message.guild
        unique_id = generate_unique_id()  # Generer et unikt ID
        opgave_content = reaction.message.content
        unikke_ids[unique_id] = {
            'user_id': user.id,
            'content': opgave_content,
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        gem_data(unikke_ids, JSON_FILE_PATH1)  # Gem opdateret opgave data til JSON-filen
        overordnet_kanal = bot.get_channel(opgave_kanal_id)
        kategori = guild.get_channel(1209483154558287932)
          # Opret en kanal med det unikke ID
        kategori = guild.get_channel(1209483154558287932)
        kanal = await guild.create_text_channel(f'opgave-{unique_id}', category=kategori)
        
        embed = discord.Embed(title="Ny opgave", description=f"Oprettet af {user.mention}")
        embed.add_field(name="Opgave ID:", value=unique_id, inline=False)
        embed.add_field(name="Indhold:", value=opgave_content, inline=False)
        
        await kanal.send(embed=embed)
        print(f'Opgavekanal oprettet: {kanal.name}')
        
        # Tilføj brugeren til kanalen
        overordnet_kanal = bot.get_channel(opgave_kanal_id)
        role_to_add = None
        if kanal.category_id == salg_kanal_id:
            role_to_add = guild.get_role(rolle_id_1)  # Tilføj den relevante rolle for salgskanalen
        elif kanal.category_id == lab_kanal_id:
            role_to_add = guild.get_role(rolle_id_2)  # Tilføj den relevante rolle for labkanalen
        
        if role_to_add:
            await user.add_roles(role_to_add)
            print(f"Tilføjet {user.name} til kanalen {kanal.name} med rollen {role_to_add.name}.")
        else:
            print("Kunne ikke tilføje rolle til brugeren.")
            
        # Slet opgavebeskeden
        await reaction.message.delete()
        
@bot.command()
async def done(ctx):
    guild = ctx.guild
    role_to_remove = guild.get_role(rolle_id_1)
    role_to_add = guild.get_role(rolle_id_2)
    await ctx.author.remove_roles(role_to_remove)
    await ctx.author.add_roles(role_to_add)
    print(f"{ctx.author.name} har fået rollen {role_to_add.name} og fjernet rollen {role_to_remove.name}.")

    # Check if the channel is under the specified category
    kategori_kanal_id = 1209483154558287932  # Erstat med den faktiske kategori-ID
    if ctx.channel.category_id == kategori_kanal_id:
        # Delete the channel
        await asyncio.sleep(3)
        await ctx.channel.delete()
        print(f"Kanalen {ctx.channel.name} er blevet slettet.")
    else:
        await ctx.send("Denne kommando kan kun bruges i en kanal under en bestemt kategori.")

@bot.command()
async def ADMIN_NULSTIL(ctx):
    global unikke_ids
    unikke_ids = {}  # Nulstil unikke_ids til en tom dictionary
    gem_data(unikke_ids, JSON_FILE_PATH1)  # Gem den nulstillede data til JSON-filen
    await ctx.send("Opgaveoplysninger er blevet nulstillet!")


# Definer og initialiser opgave_data globalt
opgave_data = {}

# Funktion til at indlæse data fra JSON-fil
def indlæs_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Gem data til JSON-fil
def gem_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Funktion til at generere et unikt ID
def generate_unique_id():
    while True:
        unique_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        if unique_id not in opgave_data:  # Brug opgave_data i stedet for unikke_ids
            return unique_id


        
@bot.command()
async def salg(ctx, *args):
    if ctx.channel.id != opgave_kanal_id:
        await ctx.send("Denne kommando kan kun bruges i opgavekanalen.")
        return
    
    antal = " ".join(args)
    salg_kanal = bot.get_channel(salg_kanal_id)
    await salg_kanal.send(f"**Salgsopgave:**\n\nAntal: {antal}\nBeskrivelse: Salgsopgave\n\nAf: {ctx.author.mention}")
    
    # Indlæs tidligere gemte opgaveoplysninger fra filen
    opgave_data = indlæs_data(JSON_FILE_PATH4)
    
    # Gem brugerens ID og opgaveindhold i opgave_data
    unique_id = generate_unique_id()
    opgave_data[unique_id] = {
        'user_id': ctx.author.id,
        'content': f"Salgsopgave:\n\nAntal: {antal}\nBeskrivelse: Salgsopgave"
    }
    
    # Gem opdaterede opgaveoplysninger til den nye fil
    gem_data(opgave_data, JSON_FILE_PATH4)
    
    # Vent i 5 sekunder
    await asyncio.sleep(5)
    
    # Slet kommandobeskeden
    await ctx.message.delete()

@bot.command()
async def lab(ctx, *args):
    if ctx.channel.id != opgave_kanal_id:
        await ctx.send("Denne kommando kan kun bruges i opgavekanalen.")
        return
    
    antal = " ".join(args)
    lab_kanal = bot.get_channel(lab_kanal_id)
    await lab_kanal.send(f"**Lab-opgave:**\n\nAntal: {antal}\nBeskrivelse: Lab opgave\n\nAf: {ctx.author.mention}")
    
    # Indlæs tidligere gemte opgaveoplysninger fra filen
    opgave_data = indlæs_data(JSON_FILE_PATH4)
    
    # Gem brugerens ID og opgaveindhold i opgave_data
    unique_id = generate_unique_id()
    opgave_data[unique_id] = {
        'user_id': ctx.author.id,
        'content': f"Lab-opgave:\n\nAntal: {antal}\nBeskrivelse: Lab opgave"
    }
    
    # Gem opdaterede opgaveoplysninger til den nye fil
    gem_data(opgave_data, JSON_FILE_PATH4)
    
    # Vent i 5 sekunder
    await asyncio.sleep(5)
    
    # Slet kommandobeskeden
    await ctx.message.delete()


@bot.command()
async def salgsover(ctx, user_id: int):
    opgave_data = indlæs_data(JSON_FILE_PATH4)
    tasks_for_user = []
    for task_id, task_data in opgave_data.items():
        if isinstance(task_data, dict) and task_data.get('user_id') == user_id:
            tasks_for_user.append((task_id, task_data))
    
    if tasks_for_user:
        embed = discord.Embed(title=f"Opgaver for bruger med ID {user_id}", color=discord.Color.blue())
        for task_id, task_data in tasks_for_user:
            embed.add_field(name=f"Opgave ID: {task_id}", value=f"Indhold: {task_data.get('content')}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Ingen opgaver fundet for bruger med ID {user_id}.")

@bot.command()
async def søg(ctx, user_id: int):
    found_tasks = []
    for task_id, task_data in unikke_ids.items():
        if isinstance(task_data, dict) and task_data.get('user_id') == user_id:
            found_tasks.append(task_id)
    if found_tasks:
        response_message = await ctx.send(f"**Opgave IDs tilknyttet bruger med ID {user_id}**:\n" + '\n'.join(found_tasks))
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
    else:
        response_message = await ctx.send(f"Ingen opgaver fundet for bruger med ID {user_id}.")
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
        await response_message.delete()

@bot.command()
async def søgopgaver(ctx, user_id: int):
    tasks_for_user = []
    for task_id, task_data in unikke_ids.items():
        if isinstance(task_data, dict) and task_data.get('user_id') == user_id:
            tasks_for_user.append((task_id, task_data))
    
    if tasks_for_user:
        embed = discord.Embed(title=f"Opgaver til bruger med ID {user_id}", color=discord.Color.blue())
        for task_id, task_data in tasks_for_user:
            embed.add_field(name=f"Opgave ID: {task_id}", value=f"Indhold: {task_data.get('content')}\nTidspunkt: {task_data.get('timestamp')}", inline=False)
        await ctx.send(embed=embed)
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
    else:
        response_message = await ctx.send(f"Ingen opgaver fundet for bruger med ID {user_id}.")
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
        await response_message.delete()

@bot.command()
async def opgaveinfo(ctx, opgave_id: str):
    opgave_data = unikke_ids.get(opgave_id)
    if opgave_data:
        embed = discord.Embed(title=f"Opgave ID: {opgave_id}", color=discord.Color.blue())
        embed.add_field(name="Indhold:", value=opgave_data.get('content'), inline=False)
        embed.add_field(name="Tidspunkt:", value=opgave_data.get('timestamp'), inline=False)
        await ctx.send(embed=embed)
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
    else:
        response_message = await ctx.send(f"Ingen opgave fundet med ID {opgave_id}.")
        await asyncio.sleep(5)  # Vent i 5 sekunder
        await ctx.message.delete()  # Slet brugerens kommandobesked efter 5 sekunder
        await response_message.delete()






# JSON-filens sti
JSON_FILE_PATH2 = 'brugere.json'

# Opret JSON-filen, hvis den ikke allerede findes
if not os.path.exists(JSON_FILE_PATH2):
    with open(JSON_FILE_PATH2, 'w') as file:
        json.dump({}, file)

# Funktion til at gemme data til JSON-fil
def gem_data2(data):
    with open(JSON_FILE_PATH2, 'w') as file:
        json.dump(data, file)

# Funktion til at indlæse data fra JSON-fil
def indlæs_data2():
    try:
        with open(JSON_FILE_PATH2, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Funktion til at tilføje en bruger til JSON-data
async def tilføj_bruger(user_id):
    brugere = indlæs_data2()
    if str(user_id) not in brugere:
        try:
            user = await bot.fetch_user(user_id)
            brugere[str(user_id)] = user.name
            gem_data2(brugere)
            return True
        except discord.NotFound:
            return False
    else:
        return False  # Returnerer False, hvis brugeren allerede eksisterer

# Funktion til at fjerne en bruger fra JSON-data
def fjern_bruger(user_id):
    brugere = indlæs_data2()
    if str(user_id) in brugere:
        del brugere[str(user_id)]
        gem_data2(brugere)
        return True
    else:
        return False  # Returnerer False, hvis brugeren ikke findes

# Funktion til at fjerne alle brugere fra JSON-data
def fjern_alle_brugere():
    gem_data2({})  # Overskriver JSON-filen med en tom dictionary

# Funktion til at skrive en oversigt over brugere
async def oversigt_over_brugere(ctx):
    brugere = indlæs_data2()
    if brugere:
        embed = discord.Embed(title="Liste over brugere", description="Her er en liste over de gemte brugere:")
        for user_id, username in brugere.items():
            embed.add_field(name=username, value=f"<@{user_id}>", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Ingen brugere gemt.")


# Definerer ID'en for den tilladte rolle
autoriseret_rolle_id = 1191626634445471766  # Erstat dette med den faktiske ID for den tilladte rolle

# Opretter en check funktion for at kontrollere, om brugeren har den tilladte rolle
def autoriseret(ctx):
    return ctx.author.roles and any(role.id == autoriseret_rolle_id for role in ctx.author.roles)

# Tilføj kommandoer
@bot.command()
@commands.check(autoriseret)  # Tilføj check funktionen til kommandoerne
async def tilføj(ctx, user_id: int):
    if await tilføj_bruger(user_id):
        await ctx.send(f"Bruger {user_id} tilføjet.")
    else:
        await ctx.send(f"Kunne ikke tilføje bruger {user_id}.")
    await ctx.message.delete()  # Sletter kun kommandobeskeden

@bot.command()
@commands.check(autoriseret)  # Tilføj check funktionen til kommandoerne
async def fjern(ctx, user_id: int):
    if fjern_bruger(user_id):
        await ctx.send(f"Bruger {user_id} fjernet.")
    else:
        await ctx.send(f"Bruger {user_id} findes ikke.")
    await ctx.message.delete()  # Sletter kun kommandobeskeden

@bot.command()
@commands.check(autoriseret)  # Tilføj check funktionen til kommandoerne
async def fjernalle(ctx):
    fjern_alle_brugere()
    await ctx.send("Alle brugere er fjernet fra listen.")
    await ctx.message.delete()  # Sletter kun kommandobeskeden

@bot.command()
@commands.check(autoriseret)  # Tilføj check funktionen til kommandoerne
async def pushere(ctx):
    await ctx.message.delete()  # Sletter kun kommandobeskeden
    await oversigt_over_brugere(ctx)

bot.run('')  # Erstat 'TOKEN' med din bot's token
