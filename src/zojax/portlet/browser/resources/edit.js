function setPortletEditLink(el)
{
    el.hover(
            function () {
                if (!$(this).hasClass('selected')) {
                    $(this).oneTime(1000, function() {
                        $('a.zojax-portlet-edit-link').remove();
                        $(this).addClass('selected');
                        $(this).append($('<a class="zojax-portlet-edit-link" href="'+el.attr('kssattr:url')+'">Edit portlet</a>'))
                    })
                }
              },
              function () {
                  if ($(this).hasClass('selected')) {
                      $(this).oneTime(1000, function() {
                          $(this).removeClass('selected');
                          $(this).find("a.zojax-portlet-edit-link:last").remove();
                  })
                }
              }
            );
    el.attr('processed', 'true');
}

function setPortletManagerEditLink(el)
{
    var elems = el.find("div.zojax-portlet");
    for (var i = 0; i < elems.length; i++)
    {
        var portlet = $(elems[i]);
        if (!portlet.attr('processed')) {
            setPortletEditLink(portlet);
        }
    }

    el.hover(
            function () {
                if (!$(this).hasClass('selected')) {
                    $(this).oneTime(1000, function() {
                        $('a.zojax-portlet-manager-edit-link').remove();
                        $(this).addClass('selected');
                        $(this).append($('<a class="zojax-portlet-manager-edit-link" href="'+el.attr('kssattr:url')+'">Edit region</a>'));
                    })
                }
              },
              function () {
                  if ($(this).hasClass('selected')) {
                    $(this).oneTime(1000, function() {
                        $(this).removeClass('selected');
                        $(this).find("a.zojax-portlet-manager-edit-link:last").remove();
                   })
                 }
              }
            );
    el.attr('processed', 'true');
}


$(document).ready(function() {
    elems = $("div.zojax-portlet-manager");
    for (var i = 0; i < elems.length; i++)
    {
        var el = $(elems[i]);
        if (!el.attr('processed')) {

            var handler = function(el) {
                return function(data) {
                    if (data=="Ok") {
                        setPortletManagerEditLink(el);
                    }
                };
            }
            $.get(el.attr('kssattr:checkurl'), handler(el));
        }
    }
});
