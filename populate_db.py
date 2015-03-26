import os
import django

def populate():
    alltags = {
        'python': add_tag('python'),
        'tutorial': add_tag('tutorial'),
        'django': add_tag('django'),
        'bottlepy': add_tag('bottlepy'),
        'bottle': add_tag('bottle'),
        'flask': add_tag('flask')
    }

    add_link(tags=[alltags['python'], alltags['tutorial']],
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")

    add_link(tags=[alltags['python']],
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_link(tags=[alltags['python'], alltags['tutorial']],
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    add_link(tags=[alltags['django'], alltags['tutorial']],
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_link(tags=[alltags['django']],
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_link(tags=[alltags['django'], alltags['tutorial']],
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    add_link(tags=[alltags['bottlepy'], alltags['bottle']],
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_link(tags=[alltags['flask'], alltags['python']],
        title="Flask",
        url="http://flask.pocoo.org")

    # Print out what we have added to the user.
    for l in Link.objects.all():
        print "Link: {0}".format(str(l))
        print l.tags.all()

def add_users(id, host, displayname, password, github, url, guid):
    l = Link.objects.get_or_create(title=title, url=url)[0]
    for tag in tags:
        l.tags.add(tag)
    return l

def add_posts(id, title, name):
    t = Tag.objects.get_or_create(name=name)[0]
    return t

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
    django.setup()
from main.models import Posts, Friends, Users
populate()