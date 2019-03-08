import instaloader

# Get instance
L = instaloader.Instaloader()

# login
L.login("jorge.costa1@protonmail.com", "jorgecosta")

# Search and Downloads public pictures with the hashtag="comidaportuguesa"
L.download_hashtag('comidaportuguesa', max_count=30,post_filter = lambda post: post.is_video == False, fast_update=False)