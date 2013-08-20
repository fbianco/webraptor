window.addEvent('domready', function()
{

    // Add effect on all the menu boxes, and the ajax request
    $('test-button').addEvents(
        {
            'click': function(event)
            {
                //prevent the page from changing (i.e. following the link)
                event.stop();
                $('test').set('send', {onSuccess: function(responseText, responseXML) {$('result').set('text', responseText);},});
                $('test').send();
            }
        });

    $('release-button').addEvents(
        {
            'click': function(event)
            {
                //prevent the page from changing (i.e. following the link)
                event.stop();
                $('release').set('send', {onSuccess: function(responseText, responseXML) {$('result').set('text', responseText);},});
                $('release').send();
            }
        });
});