import instaloader
from instaloader import Post

L = instaloader.Instaloader()

SHORTCODE = "DT2nP7bjdis"
post = Post.from_shortcode(L.context, SHORTCODE)

L.download_post(post, target=SHORTCODE)
