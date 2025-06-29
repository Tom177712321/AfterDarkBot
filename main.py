from keep_alive import keep_alive
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# GENDER ROLES
GENDER_MAN = "Man"
GENDER_WOMAN = "Woman"
GENDER_CUSTOM = "Custom Pronouns"

# PATHS with gendered progression roles
ROLE_PATHS = {
    "Dom": {
        10:
        ("Dom-In-Training 🖤(DOM lvl 10)", "Domme-In-Training 💋(DOM lvl 10)"),
        20: ("Power Top 🕶️(DOM lvl 20)", "Queen of Control 👑(DOM lvl 20)"),
        30:
        ("Rough Handler 💪(DOMlvl 30)", "Commanding Mistress 💄(DOM lvl 30)"),
        40:
        ("Obedience Breaker 🔥(DOM lvl 40)", "Leather Matriarch 👠(DOM lvl 40)"),
        50:
        ("Master of Submission 👑(DOM lvl 50)", "Supreme Domme 🔮(DOM lvl 50)")
    },
    "Sub": {
        10: ("Submissive Boy 🧎‍♂️(Sub lvl 10)",
             "Submissive Girl 🧎‍♀️(Sub lvl 10)"),
        20: ("Obedient Plaything 🩸(Sub lvl 20)", "Eager Toy 💖(Sub lvl 20)"),
        30: ("Bound & Ready ⛓️(Sub lvl 30)", "Leashed Beauty 👠(Sub lvl 30)"),
        40:
        ("Mistress’s Good Boy 💞(Sub lvl 40)", "Sir’s Favorite 😈(Sub lvl 40)"),
        50: ("Owned & Trained 🔐(Sub lvl 50)", "Owned & Obedient 💍(Sub lvl 50)")
    },
    "BDSM": {
        10: ("Curious Sadist/madsochist 🧨🧵 (BDSM lvl 10)",
             "Curious Sadist/madsochist 🧨🧵 (BDSM lvl 10)"),
        20: ("Pain Dealer 🩹 (BDSM lvl 20)", "Whip Enthusiast 🔥(BDSM lvl 20)"),
        30:
        ("Restraint Artist 🔒(BDSM lvl 30)", "Rope Temptress 🪢(BDSM lvl 30)"),
        40:
        ("Dungeon Dweller 🕳️(BDSM LVL 40)", "Dungeon Queen 🎭(BDSM lvl 40)"),
        50: ("Master of the Scene 🎬(BDSM lvl 50)",
             "Mistress of Pain 💉(BDSM lvl 50)")
    },
    "DD/lg & caregiver": {
        10:
        ("Soft Daddy 🧸(Caregiver lvl 10)", "Sweet Mommy 🍪(Caregiver lvl 10)"),
        20: ("Gentle Caretaker 💞(Caregiver lvl 20)",
             "Nurturing Guardian 🌼(Caregiver lvl 20)"),
        30: ("Affirmation Giver 📜(Caregiver lvl 30)",
             "Cuddle Queen 🧦(Caregiver lvl 30)"),
        40: ("Emotional Anchor ⚓(Caregiver lvl 40)",
             "Lovey Disciplinarian 📚(Caregiver lvl 40)"),
        50: ("Big Daddy Energy 🌟(Caregiver lvl 50)",
             "Divine Mommy ✨(Caregiver lvl 50)")
    },
    "PetPlay": {
        10:
        ("Frisky Pup 🐶(Petplay lvl 10)", "Playful Kitten 🐱(Petplay lvl 10)"),
        20: ("Loyal Pet 🐾(Petplay lvl 20)", "Collared Pet 🐕(Petplay lvl 20)"),
        30: ("Obedient Beast 🦴(Petplay lvl 30)",
             "Trained Kitty 🎀(Petplay lvl 30)"),
        40: ("Cage Dweller ⛓️(Petplay lvl 40)",
             "Leash Princess 💖(Petplay lvl 40)"),
        50: ("Alpha 🐺(Petplay lvl 50)", "Master’s Favorite 💎(Petplay lvl 50)")
    },
    "Exhibisionist": {
        10: ("Peek Tease 👀(Exhibitionist lvl 10)",
             "Flash Babe 🌟(Exhibitionist lvl 10)"),
        20: ("Skin Dropper 💦(Exhibitionist lvl 20)",
             "Flash Princess 💋(Exhibitionist lvl 20)"),
        30: ("Street Flasher 🚨(Exhibitionist lvl 30)",
             "No-Panty Princess 🩲(Exhibitionist lvl 30)"),
        40: ("Live Show Off 🔴(Exhibitionist lvl 40)",
             "Nudes Muse 🎞️(Exhibitionist lvl 40)"),
        50: ("Public King 👑(Exhibitionist lvl 50)",
             "Public Queen 👑(Exhibitionist lvl 50)")
    },
    "voyeur": {
        10: ("Curious Gazer 👁️(Voyeur lvl 10)",
             "Naughty Watcher 📹(Voyeur lvl 10)"),
        20: ("Secret Observer 🕵️‍♂️(Voyeur lvl 20)",
             "Peep Show Fan 👀(Voyeur lvl 20)"),
        30: ("Shadow Lurker 🌒(Voyeur lvl 30)",
             "Hidden Cam Princess 🎥(Voyeur lvl 30)"),
        40:
        ("Orgasm Witness 🔥(Voyeur lvl 40)", "Pleasure Spy 🧿(Voyeur lvl 40)"),
        50: ("Master Voyeur 👁️‍🗨️(Voyeur lvl 50)",
             "Queen of Shadows 🕶️(Voyeur lvl 50)")
    }
}


async def assign_path_roles(member, level):
    user_roles = [role.name for role in member.roles]
    has_man = GENDER_MAN in user_roles
    has_woman = GENDER_WOMAN in user_roles
    has_custom = GENDER_CUSTOM in user_roles

    for path, levels in ROLE_PATHS.items():
        if path in ["Dom", "Sub"]:
            if "Switch" in user_roles or path in user_roles:
                pass  # continue with check
            else:
                continue
        elif path not in user_roles:
            continue  # skip if user doesn't have this path

        for lvl, (man_role, woman_role) in sorted(levels.items(),
                                                  reverse=True):
            if level >= lvl:
                guild = member.guild
                role_m = discord.utils.get(guild.roles, name=man_role)
                role_w = discord.utils.get(guild.roles, name=woman_role)

                # Cleanup lower level roles (optional)
                for old_lvl, (old_man, old_woman) in levels.items():
                    if old_lvl < lvl:
                        r_m = discord.utils.get(guild.roles, name=old_man)
                        r_w = discord.utils.get(guild.roles, name=old_woman)
                        if r_m and r_m in member.roles:
                            await member.remove_roles(r_m)
                        if r_w and r_w in member.roles:
                            await member.remove_roles(r_w)

                # Assign based on gender role
                if has_custom:
                    if role_m and role_m not in member.roles:
                        await member.add_roles(role_m)
                    if role_w and role_w not in member.roles:
                        await member.add_roles(role_w)
                elif has_man:
                    if role_m and role_m not in member.roles:
                        await member.add_roles(role_m)
                elif has_woman:
                    if role_w and role_w not in member.roles:
                        await member.add_roles(role_w)

                print(
                    f"✅ Assigned {path} level {lvl} roles to {member.display_name}"
                )
                break


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == "level-logs" and "leveled up to level" in message.content:
        try:
            user = message.mentions[0]
            level = int(message.content.split()[-1].replace("!", ""))
            await assign_path_roles(user, level)
        except Exception as e:
            print(f"⚠️ Error processing level-up: {e}")

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"🚀 Bot is online as {bot.user}")


# Paste your bot token here
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
