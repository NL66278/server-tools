// Replace openerp_announcement var, defined in mail addon, by a version
// just passing through the show_application method.
openerp_announcement = function(instance) {
    instance.web.WebClient.include({
        show_application: function() {
            return this._super.apply(this, arguments);
        },
    });
};
