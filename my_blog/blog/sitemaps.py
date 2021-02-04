from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSitemap(Sitemap):
    # How often a blog post is added/updated.
    changefreq = 'weekly'
    # how relevant blog posts are to the website.
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
