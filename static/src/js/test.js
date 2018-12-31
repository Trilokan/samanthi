odoo.define('web.moris', function (require) {
"use strict";

var config = require('web.config');
var core = require('web.core');

var _t = core._t;
var QWeb = core.qweb;


return core.Class.extend({
    process_moris: function($sheet) {
        var $new_sheet = this.render_element('FormRenderingSheet', $sheet.getAttributes());
        this.handle_common_properties($new_sheet, $sheet);
        var $dst = $new_sheet.find('.o_form_sheet');
        $sheet.contents().appendTo($dst);
        $sheet.before($new_sheet).remove();
        this.process($new_sheet);
    },


});

console.log(core);
});