'use strict';

/*
 * This module uses jQuery.
 */

/**
 * This file exports one object: the namespace "charMover".
 */
var charMover = {};

charMover.CharMover = function(tagName, regexp, xDist, yDist) {
    this.elts = $(tagName);
    for (var i = 0; i < this.elts.length; i++) {
        var elt = this.elts.eq(i);
        var html = elt.html().replace(regexp, "<span class='moving'>$&</span>");
        elt.html(html);
    }

    this.spans = $(tagName + " span.moving");
    for (var i = 0; i < this.spans.length; i++) {
        var top = String(charMover.randomFromTo(-yDist, yDist));
        var left = String(charMover.randomFromTo(-xDist, xDist));
        this.spans[i].style.top = top + "px";
        this.spans[i].style.left = left + "px";
    }

    this.elts.css({ display: "block" });
};

charMover.randomFromTo = function(from, to) {
    return Math.floor(Math.random() * (to - from + 1) + from);
};
