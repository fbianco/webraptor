webraptor
=========

Webraptor is a minimalist template based static HTML website generator
additionned by a JS and CSS compression. The template are based on python
and HTML using pyTenjin. The compression requires yui-compressor from Yahoo!.

Licenses
--------

This python code is available under the GPL v3. The example HTML, CSS code and
other images are released under a CC-BY-SA. The effect JS is under an MIT
license. Please refer to content of the files.

Note about pyTenjin and other codes
-----------------------------------

A copy of these codes is provided in this repository.

*pyTenjin is provided under an MIT License. [Upstream code is available
there](http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html).*

*Mootools, Menumatic, blueprint.css under MIT or MIT-like licences. Refer to
there websites for more details.*

Example
-------

Go to example folder to see compiled pages with webraptor. Browse to content
for the pages and templates for the pages templates.

How to use webraptor
--------------------

Edit the config.py file to specify the location of your files.

The content folder stores the partial HTML pages.

The templates folder stores the pages template with pyTenjin syntax.

Start by editing the YAML menu file /content/menu.yml to add remove page from
the menu. The pages are generated based on the list provided in this file. The
possible options for the menu items are:

* name: page name in complete and readable text, the corresponding page is all
  lower case letter and spaces replaced by underscore. Special caracters are
  replaced by simple letters (i.e é,ê,è->e).
* displayinmenu: [True, False] if the entry appears in menu or not. This is
  usefull to compile index page or error pages you do not want to see in menu.
* title: page title in HTML header, if not provided the page name is used.
* onepage: [True, False] if true the submenus item are considered as local
  anchor in the menu page.
* submenus:
    * to create a submenu add an indented list of pagename in complete and
      readable text.
    * If you want special menu name you can use a combination of name (what
      appears in menu, and pagename, the real page name)
    * Use name/pagename combination to by-pass the onepage options on someitems.
* If the pages specified in the menu are stored in the content folder with .yml
  extension. The file is parsed as a YAML file. This requires:
    * title: The page title for html header
    * template: the template name stored in templates folder
    * then follow your custom YAML structure used to feed your template.

Compression
-----------

CSS and JS compression requires yui-compressor and is based on a simple shell
script, this will only work in unix-like systems.

Admin page
----------

If your webserver provide a way to run python scritps, you can use the
index.html file to preview and release your website. You will probably need to
add special rights on folder to allow python to rewrite your pages.
