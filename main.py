import discord, asyncio, json, datetime, os.path, math

import settings

class Sparrow(discord.Client):
	async def sleep_till_reset(self, curr : datetime.datetime):
		next_reset_h = math.ceil(curr.hour / self.settings.interval) * self.settings.interval
		if next_reset_h == 24:
			next_reset_day = curr.today() + datetime.timedelta(days=1)
			next_reset_h = 0
		else:
			next_reset_day = curr.today()

		next_reset_obj = curr.replace(day=next_reset_day.day, hour=next_reset_h, minute=0, second=0, microsecond=0)

		diff = next_reset_obj - curr
		await asyncio.sleep(diff.total_seconds())

		return

	# TODO: Maybe reload config file here?
	async def hour_to_pfp(self, hour : int):
		pfp_index = int(hour / self.settings.interval)

		item = self.settings.rotation[pfp_index]
		try:
			fpath = os.path.join(self.settings.root, item[0])
		except AttributeError:
			fpath = item[0]

		avi = open(fpath, "rb")
		await self.user.edit(avatar=avi.read())

		try:
			status = discord.Game(self.settings.global_status)
		except AttributeError:
			status = discord.Game(item[1])

		await self.change_presence(status=discord.Status.online, activity=status)

		return

	# TODO: there's a small chance that this function
	# changes the profile picture in a very short interval
	# and it can't handle Discord's error if it does happen.
	# Reference: discord.errors.HTTPException
	async def timercycle(self):
		# `interval` is how many hours between a change.
		# In this case, it's 24 hours divided by how many profile pictures we have.
		self.settings.interval = int(self.settings.cycle / len(self.settings.rotation))

		curr_time = datetime.datetime.now()
		await self.hour_to_pfp(curr_time.hour)

		while True:
			await self.sleep_till_reset(curr_time)
			curr_time = datetime.datetime.now()
			await self.hour_to_pfp(curr_time.hour)

	async def on_ready(self):
		print("Logged in as", self.user)

		asyncio.create_task(self.timercycle())

if __name__ == "__main__":
	import sys

	client = Sparrow()
	try:
		cfg_path = sys.argv[1]
	except IndexError:
		cfg_path = "config.json"

	fp = open(cfg_path)
	json_out = json.load(fp)
	fp.close()

	client.settings = settings.Config(json_out)
	client.run(client.settings.token)

