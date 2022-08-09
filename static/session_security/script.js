// console.log("Starting Security")
if (window.yourlabs === undefined){
    // console.log("Undefined")
    window.yourlabs = {};
}
else{
    // console.log("Defined")
}



yourlabs.SessionSecurity = function(options) {

    this.$warning = $('#session_security_warning');
    this.lastActivity = new Date();

    this.events = ['mousemove', 'scroll', 'keyup', 'click', 'touchstart', 'touchend', 'touchmove'];

    $.extend(this, options);

    var $document = $(document);
    for(var i=0; i<this.events.length; i++) {
        if ($document[this.events[i]]) {
            $document[this.events[i]]($.proxy(this.activity, this));
        }
    }
    this.apply()

    if (this.confirmFormDiscard) {
        window.onbeforeunload = $.proxy(this.onbeforeunload, this);
        $document.on('change', ':input', $.proxy(this.formChange, this));
        $document.on('submit', 'form', $.proxy(this.formClean, this));
        $document.on('reset', 'form', $.proxy(this.formClean, this));
    }
}

yourlabs.SessionSecurity.prototype = {

    expire: function() {
        this.expired = true;
        // this.returnToUrl = "logout";

        if (this.returnToUrl !== undefined) {
            window.location.href = this.returnToUrl;
        }
        else {
            // console.log(session_security.utils.get_last_activity);
            window.location.href = 'logout'
            // window.location.reload();
        }
    },

    showWarning: function() {
        this.$warning.fadeIn('slow');
        this.$warning.attr('aria-hidden', 'false');
        $('.session_security_modal').focus();
        $.ajax({
            url:'save_last_activity',
            // type:'GET',
            // data:{},
            // dataType:'json',
        });
    },

    hideWarning: function() {
        this.$warning.hide();
        this.$warning.attr('aria-hidden', 'true');
    },

    activity: function() {
        var now = new Date();
        if (now - this.lastActivity < 1000)

            return;

        this.lastActivity = now;

        if (this.$warning.is(':visible')) {
            this.ping();
        }

        this.hideWarning();
    },

    ping: function() {
        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);

        $.ajax(this.pingUrl, {
            data: {idleFor: idleFor},
            cache: false,
            success: $.proxy(this.pong, this),

            error: $.proxy(this.apply, this),
            dataType: 'json',
            type: 'get'
        });
    },

    pong: function(data) {
        if (data === 'logout') return this.expire();

        this.lastActivity = new Date();
        this.lastActivity.setSeconds(this.lastActivity.getSeconds() - data);
        this.apply();
    },

    apply: function() {
        clearTimeout(this.timeout);

        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);

        if (idleFor >= this.expireAfter) {
            return this.expire();
        } else if (idleFor >= this.warnAfter) {
            this.showWarning();
            nextPing = this.expireAfter - idleFor;
        } else {
            this.hideWarning();
            nextPing = this.warnAfter - idleFor;
        }

        this.timeout = setTimeout($.proxy(this.ping, this), nextPing * 1000);
    },

    onbeforeunload: function(e) {
        if ($('form[data-dirty]').length && !this.expired) {
            return this.confirmFormDiscard;
        }
    },

    formChange: function(e) {
        $(e.target).closest('form').attr('data-dirty', true);
    },

    formClean: function(e) {
        $(e.target).removeAttr('data-dirty');
    }
}