$(document).ready(function(){
    $('.z-portlet-preview-content-wrapper a').click(function() {
        if (this.href && this.href != '#')
            top.location = this.href;
    }
    )
});