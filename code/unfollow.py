from instabot import Bot
import my_config
from compareArrays import compareArrs
import time



#fix ds_user error
import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
os.remove(cookie_del[0])


#unfollow accounts w/ instabot
bot = Bot()
bot.login(username=my_config.USER,
          password=my_config.PASSWORD)
# followers = set(bot.followers())















# import instaloader
#get insta profile info w/ instaloader
# L = instaloader.Instaloader()
# L.login(config.USER, config.PASSWORD)
# profile = instaloader.Profile.from_username(L.context, config.USER)
# followers = list(profile.get_followers())

# for i in range(len(followers)):
#     followers[i] = followers[i].username