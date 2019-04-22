import argparse
import praw
import time

parser = argparse.ArgumentParser(description="A script to unhide posts on Reddit.")
parser.add_argument("-u", "--username", help="Username to log into Reddit with.", action="store")
parser.add_argument("-p", "--password", help="Password to log into Reddit with.", action="store")
parser.add_argument("-d", "--days-to-keep", help="The number of days of posts to not unhide.", type=int, default=1, action="store")
parser.add_argument("-s", "--secret", help="Script Secret", action="store")
parser.add_argument("-c", "--client_id", help="Script client_id", action="store")
parser.add_argument("-m", "--max_count", help="Maximum number of posts to unhide. Use negative value or don't use it for all.", type=int, default=-1, action="store")
args = parser.parse_args()

if args.days_to_keep < 0:
	args.days_to_keep = 0


reddit = praw.Reddit(client_id=args.client_id, client_secret=args.secret,
                     password=args.password, user_agent='reddit-unhider',
                     username=args.username)

time_cutoff = int(time.time()) - (args.days_to_keep * 60 * 60 * 24)
num_hidden = 0
after = None
no_more = False
while not no_more:
	hidden_posts = reddit.user.me().hidden(limit=None, params={"after" : after})
	no_more = True
	for post in hidden_posts:
		no_more = False
		if int(post.created_utc) >= time_cutoff or (args.max_count >= 0 and num_hidden >= args.max_count):
			after = post.name
			continue
		print ("[{}] Unhiding [{}] ... ".format(num_hidden+1, post.title))
		post.unhide()
		num_hidden += 1

print ("\n{} posts unhidden!".format(num_hidden))
