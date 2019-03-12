import instaloader



# Get instance
loader = instaloader.Instaloader()

# login
loader.login("jorge.costa1@protonmail.com", "jorgecosta")

# Search and Downloads public pictures with the hashtag="comidaportuguesa"
loader.download_hashtag(, max_count=30,post_filter = lambda post: post.is_video == False, fast_update=True)