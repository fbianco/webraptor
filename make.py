#!/usr/bin/python
# -*- coding: utf-8 -*-
import tenjin
from tenjin.helpers import *
import os
import cgi
import subprocess
import cgitb
import yaml
import locale
import time
import re

engine = tenjin.Engine()

import config
filesdir = os.path.normpath(config.filesdir)
contentdir = os.path.join(filesdir,'content')
templatedir = os.path.join(filesdir,'templates')
generatedir = os.path.join(filesdir,'')

DEBUG = False
WEB = False # Whether one uses the index.html console or not to output html

if DEBUG:
    cgitb.enable(format='text')
else:
    cgitb.enable(display=0, logdir="log")

form = cgi.FieldStorage()

preview = form.getvalue("preview",False) == "True"
if preview :
    compressed = False
    generatedir = os.path.join(filesdir,'preview')
else:
    compressed = True
    
if DEBUG:
    compressed = False

singlelang = True  # Do not use multilang website
lang = 'en' # a string for singlelang website
# For multilang you can create page whith name -lang.html
# and specify a list of lang
#lang = ('en','fr') 
cache = {}

error404 = """
<h1>Error 404</h1>
<p>Page doesn't exist.</p>
    """

def menus():
    """Create the menu """
    if not cache.has_key('menus'):
        cache['menus'] = render('menu')
    return cache['menus']

def news():
    """Get news"""
    if not cache.has_key('news'):
        cache['news'] = render('news')
    return cache['news']

def date():
    """Get the date in the correct locale"""

    if not cache.has_key('date'):
        if 'fr' == lang:
            locale.setlocale(locale.LC_ALL, 'fr_CH.UTF-8')
        elif 'en' == lang:
            pass
        elif 'de' == lang:
            pass
        else:
            print "Unknown lang"

        cache['date'] = time.strftime('%d %B %Y',time.localtime())

    return cache['date']

def simplename(s):
    """Simplify name"""
    s = s.lower()
    s = re.sub(u'ê|ë|é|è', 'e', s, count=0)
    s = re.sub(u'â|ä|á|à','a', s, count=0)
    s = re.sub(u'ô|ö|ó','o', s, count=0)
    s = re.sub(u'û|ü|ú|ù','u', s, count=0)
    s = re.sub(u'î|ï|í','i', s, count=0)
    s = re.sub('\s','_', s, count=0)
    return s

def filepath(s,ext):
    """Return whole path to filename"""
    if singlelang:
        return os.path.join(contentdir,s+'.'+ext)
    else:
        return os.path.join(contentdir,s+'-'+lang+'.'+ext)

def render(name,template=None):
    """Render a file with tenjin template """

    o = error404

    if name is None:
        return error404

    name, ext = os.path.splitext(name)

    # no extension specified
    if '' == ext :
        if os.path.exists(filepath(name,'yml')):
            ext = 'yml'
        elif os.path.exists(filepath(name,'html')):
            ext = 'html'
        else:
            print "Error 404: Missing file or template for %s, no page will be generated." % (name,)
            return error404

    try:
        if 'yml' == ext:
            if template is None:
                template = name + '.pyhtml'
            with open(filepath(name,'yml')) as f:
                c = yaml.load(f)
                o = engine.render(os.path.join(templatedir,template), c )
        elif 'html' == ext:
            with open(filepath(name,'html')) as f:
                o = f.read()
    except IOError:
        print "Error 404: Missing file or template for %s, no page will be generated." % (name,)
        return error404
    else:
        return o

def createpage(pagetitle,maintitle=None,summary=None):
    """Render a page and save it in a file
        @maintitle is the menu name for submenu pages
    """

    pagename = simplename(pagetitle)
    if maintitle is None:
        maintitle = pagetitle # we are generating a main page

    c = {
        'title' : pagetitle,
        'maintitle': maintitle,
        'pageurl': pagename,
        'menu' : menus(),
        'summary': summary,
        'news' : news(),
        'date' : date(),
        'content' : render(pagename),
        'compressed' : compressed, # compress js and css
        }
    if singlelang:
        o = engine.render(os.path.join(templatedir,'template.pyhtml'), c )
        f = file(os.path.join(generatedir,pagename+'.html'),'w')
        f.write(o)
        f.close()
    else:
        o = engine.render(os.path.join(templatedir,'template-'+lang+'.pyhtml'), c )
        f = file(os.path.join(generatedir,lang,pagename+'.html'),'w')
        f.write(o)
        f.close()

def generate():
    """Generate the whole website"""

    if singlelang:
        with open(os.path.join(contentdir,'menu.yml')) as f:
            c = yaml.load(f)
    else:
        for l in lang:
            with open(os.path.join(contentdir,'menu-'+l+'.yml')) as f:
                c = yaml.load(f)


    for menu in c['menus']:
        group = simplename(unicode(menu['name']))

        # This shows how to add custom keys to the templates from the menu.yml file
        if not menu.has_key('summary') :
            summary = ''
        else:
            summary = menu['summary']

        if menu.has_key('displayinmenu') and False == menu['displayinmenu']:
            createpage(menu['name'],menu['title'],summary)

        elif (menu.has_key('onepage') and True == menu['onepage']) or not menu.has_key('submenus') :
            print "Rendering page %s" % (menu['name'],)
            createpage(menu['name'],summary=summary)
        elif menu.has_key('submenus'):
            for page in menu['submenus']:
                if type(page)==type({}):
                    page = page['pagename']
                print "Rendering page %s" % (unicode(page),)
                createpage(unicode(page),menu['name'],summary=summary)

    if compressed:
        print "Compressing scripts and style sheets, it can take a while."
        fstdout = open(os.path.join(generatedir,'compress.log'),'w')
        fsterr = open(os.path.join(generatedir,'compress.err'),'w')
        o = subprocess.Popen(['/bin/sh','compress.sh'],
            cwd=os.path.join(filesdir,'css'), stdin=None,stdout=fstdout, stderr=fsterr)
        o = rc = subprocess.Popen(['/bin/sh','compress.sh'],
            cwd=os.path.join(filesdir,'js'), stdin=None, stdout=fstdout, stderr=fsterr)
        fstdout.close()
        fsterr.close()

    print "Job finished"

if __name__ == "__main__":

    if WEB:
        print "Content-Type: text/html; charset=utf-8\n"

    generate()
