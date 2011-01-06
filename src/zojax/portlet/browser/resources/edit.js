function setPortletEditLink(el)
{
    el.hover(
            function () {
                if (!$(this).hasClass('selected')) {
                    $(this).addClass('selected');
                    $(this).append($('<a class="zojax-portlet-edit-link" href="'+el.attr('kssattr:url')+'">Edit portlet</a>'))
                    $(this).find("a.zojax-portlet-edit-link").hide();
                    $(this).find("a.zojax-portlet-edit-link").delay(350).fadeIn(200);
                }
              },
              function () {
                  if ($(this).hasClass('selected')) {
                      $(this).removeClass('selected');
                      $(this).find("a.zojax-portlet-edit-link:last").remove();
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
                    $(this).addClass('selected');
                    $(this).append($('<a class="zojax-portlet-manager-edit-link" href="'+el.attr('kssattr:url')+'">Edit region</a>'));
                    $(this).find("a.zojax-portlet-manager-edit-link").hide();
                    $(this).find("a.zojax-portlet-manager-edit-link").delay(250).fadeIn(200);
                }
              },
              function () {
                  if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    $(this).find("a.zojax-portlet-manager-edit-link:last").remove();
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
                    setPortletManagerEditLink(el);
                };
            }     
            $.get(el.attr('kssattr:url'), handler(el))
        }
    }
});
