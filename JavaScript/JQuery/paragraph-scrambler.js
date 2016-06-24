'use strict';

/*
 * This module uses jQuery.
 */

/**
 * This file exports one object: the namespace "scrambler".
 */
var scrambler = {};

scrambler.Scrambler = function(tagName) {
    this.elts = $(tagName);
};

scrambler.Scrambler.prototype.scramble1 = function () {
    var elt = this.elts.eq(this.randomFromTo(0, this.elts.length - 1));
    this.scrambleEltText(elt);
};

scrambler.Scrambler.prototype.scrambleEltText = function (elt) {
    var text = elt.html();
    var i1 = this.randomFromTo(0, text.length - 1);
    var i2 = this.randomFromTo(0, text.length - 2);
    if (i2 >= i1) {
        ++i2;
    }
    var newText = this.swapChars(text, i1, i2);
    elt.html(newText);
};

scrambler.Scrambler.prototype.swapChars = function(text, i1, i2) {
    if (i1 == i2) {
        return text;
    }
    if (i1 > i2) {
        var temp = i2;
        i2 = i1;
        i1 = temp;
    }
    var c1 = text.charAt(i1);
    var c2 = text.charAt(i2)
    return text.slice(0, i1) + c2 + text.slice(i1+1, i2) + c1 +
        text.slice(i2+1, text.length);
};

scrambler.Scrambler.prototype.randomFromTo = function(from, to) {
    return Math.floor(Math.random() * (to - from + 1) + from);
};
