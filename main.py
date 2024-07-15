"""
Nejo - A protection bot for Discord.
Copyright (C) 2024 ItsAsheer, NejoBot developers and external contributers.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import nextcord
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

intents = nextcord.Intents.default()
intents.members = True

client = nextcord.Client(intents=intents)

BLACKLIST_URL = "https://kickthespy.pet/ids"

def get_blacklisted_ids():
    try:
        response = requests.get(BLACKLIST_URL)
        response.raise_for_status()
        ids = response.text.splitlines()
        return set(ids)
    except requests.RequestException as e:
        logging.error(f"Error fetching blacklist: {e}")
        return set()

blacklisted_ids = get_blacklisted_ids()

@client.event
async def on_ready():
    logging.info(f'Bot connected as {client.user}')

@client.event
async def on_member_join(member):
    if str(member.id) in blacklisted_ids:
        try:
            await member.send("You are blacklisted, as you probably are spy.pet. Contact Nejo Developers for more information.")
        except nextcord.Forbidden:
            logging.warning(f"Could not send DM to {member.name}")
        await member.kick(reason="User is blacklisted")

def load_token():
    try:
        with open('env.json') as f:
            data = json.load(f)
            return data['token']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logging.error(f"Error loading token: {e}")
        return None

token = load_token()
if token:
    client.run(token)
else:
    logging.error("Bot token not found. Exiting.")
