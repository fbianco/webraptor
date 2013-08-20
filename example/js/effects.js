// © François Bianco, under MIT license.

window.addEvent('domready', function()
{
    /*Create a MenuMatic Instance*/
    var myMenu = new MenuMatic();

    /* News rotate */
    var NewsRotate = new Class({
        initialize:function() {

            var newsControl = new Element('ul', {id: 'newscontrol'}).inject($('news'),'top');

            var i = 0;
            $$('#news div').each( function(el) {
                el.setStyles({display:'none', opacity:'0'});
            });
            $$('#news div.recent').each( function(el) {
                el.set({id:'news'+i, 'morph':{duration: 'long'}});
                var button = new Element('li', {
                                id: 'ctrl'+i,
                                'class': 'inactive',
                                text: ' ',
                                events: {
                                    click: function() {
                                        displayNews(el);
                                        this.set({'class':'active'});
                                        currentCtrl = this;
                                    },
                                },
                            }).inject(newsControl);
                i++;
            });
            var len = i;

            if(len == 0)
                return

            var current = 0;
            var currentNews = $('news0');
            var currentCtrl = $('ctrl0');
            currentCtrl.set({'class':'active'});
            currentNews.setStyles({display:'block', opacity:'1'});

            function displayNews(el) {

                currentNews.morph({opacity:'0'});
                currentNews.setStyles({display:'none'});

                currentNews = el;
                currentNews.setStyles({display:'block'});
                currentNews.morph({opacity:'1'});

                currentCtrl.set({'class':'inactive'});
            };

            function displayNextNews() {
                current = (current+1) % len;
                displayNews($('news'+current));
                currentCtrl = $('ctrl'+current);
                currentCtrl.set({'class':'active'});
            };

            displayNextNews.periodical(8000);
        },
    });

    var loadNews = new Request.HTML({
        url: 'content/news.html',
        method: 'get',
        update: $('news'),
        onRequest: function(){
            $('news').set('html','<h2>Loading …</h2>');
            },
        onComplete: function(){
            var newsRotate = new NewsRotate();
            },
        });
     loadNews.send()


    /* Social button horizontal accordion */
    // # FIXME store it in a class
    var AccordionTab = new Class({
        initialize:function() {
            var opened;
            var lengthClosed = '30px';
            var lengthOpened = '150px';
            $$('#social div').each( function(el) {
                el.set({'morph':{duration: 'long'}});
                var button = new Element('div', {
                    'class': 'btn',
                    text: ' ',
                    events: {
                        mouseover: function() {
                            opened.morph({'width':lengthClosed});
                            el.morph({'width':lengthOpened});
                            opened = el;
                            },
                        },
                    }).inject(el,'top');
                opened = el;
            });
            opened.set({'style':'width:'+lengthOpened});
        },
    });

    var socialTab = new AccordionTab();

    /* Email field emptying on focus */
    var AutoEmptyEmail = new Class({
        initialize:function(id){
            el = $(id);
            var defaultValue = el.value;
            el.addEvents({
                'focus': function(){this.value='';},
                'blur': function(){if( this.get('value') == "" ) this.set('value',defaultValue);
                },
            });
        },
    });

    var topEmail = new AutoEmptyEmail('topemail');
    var centeremail = new AutoEmptyEmail('centeremail');

});