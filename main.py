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
        10: (1388768247301541989, 1388768392336510976),
        20: (1388768474226102366, 1388768552705724497),
        30: (1388768596427018260, 1388768661061500938),
        40: (1388768748655345725, 1388768819312459908),
        50: (1388768905232777377, 1388768956432646155)
    },
    "Sub": {
        10: (1388769298335662204, 1388769417915138159),
        20: (1388769498953285692, 1388769610282831872),
        30: (1388769679480324177, 1388769749890236507),
        40: (1388769954265825401, 1388770010394267658),
        50: (1388770102949711892, 1388770173296840724)
    },
    "BDSM": {
        10: (1388771792549580810, 1388772106648424528),
        20: (1388772188571570176, 1388772277784543262),
        30: (1388772358503796736, 1388772428267913336),
        40: (1388772541564325988, 1388772608379453551),
        50: (1388772745550233630, 1388772796422946846)
    },
    "DD/lg & caregiver": {
        10: (1388772909186547782, 1388773047636328510),
        20: (1388773265073377302, 1388773320077611068),
        30: (1388773376432017488, 1388773483122786365),
        40: (1388773573946118154, 1388773645006147645),
        50: (1388773717299167262, 1388773808416100445)
    },
    "PetPlay": {
        10: (1388773985864515584, 1388774063861927946),
        20: (1388774136112742510, 1388774209722781757),
        30: (1388774292564480001, 1388774354883579905),
        40: (1388774470726062131, 1388774534164906014),
        50: (1388774731532075068, 1388774814180704339)
    },
    "Exhibisionist": {
        10: (1388774975720263732, 1388775114883072183),
        20: (1388775200027312239, 1388775266016559124),
        30: (1388775373189414922, 1388775456353947659),
        40: (1388775589447598161, 1388775657613426708),
        50: (1388775724294471790, 1388775945615446207)
    },
    "voyeur": {
        10: (1388776179665731625, 1388776257348436018),
        20: (1388776324813951069, 1388776381961338950),
        30: (1388776476941226045, 1388776529353511063),
        40: (1388776623716831293, 1388776668260466719),
        50: (1388776728184230020, 1388776813974650960)
    }
}

MAN_ROLE_ID = 1387893566302589049
WOMAN_ROLE_ID = 1387893469544054844
CUSTOM_ROLE_ID = 1387893702227263587

async def assign_path_roles(member, level):
    role_ids = [role.id for role in member.roles]
    has_man = MAN_ROLE_ID in role_ids
    has_woman = WOMAN_ROLE_ID in role_ids
    has_custom = CUSTOM_ROLE_ID in role_ids

    for path, levels in ROLE_PATHS.items():
        if path in ["Dom", "Sub"]:
            if any(role.name == "Switch" or role.name == path for role in member.roles):
                pass
            else:
                continue
        elif not any(role.name == path for role in member.roles):
            continue

        for lvl, (man_role_id, woman_role_id) in sorted(levels.items(), reverse=True):
            if level >= lvl:
                guild = member.guild
                # Remove old roles
                for old_lvl, (old_man_id, old_woman_id) in levels.items():
                    if old_lvl < lvl:
                        old_man = guild.get_role(old_man_id)
                        old_woman = guild.get_role(old_woman_id)
                        if old_man in member.roles:
                            await member.remove_roles(old_man)
                        if old_woman in member.roles:
                            await member.remove_roles(old_woman)

                # Assign new roles
                role_m = guild.get_role(man_role_id)
                role_w = guild.get_role(woman_role_id)

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

                print(f"✅ Assigned {path} level {lvl} roles to {member.display_name}")
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
