/*
 * This module uses jQuery.
 */

/**
 * This file exports one object: the namespace "htmlhider".
 */
var htmlhider = {};

htmlhider.HTMLHider = function(tagName) {
    var elts = document.getElementsByTagName(tagName);
    // Transfer elements from the array-like object to a real array, in random
    // order
    this.remainingElts = [];
    for (var i = 0; i < elts.length; i++) {
        var insIndex = htmlhider.randomFromTo(0, this.remainingElts.length);
	this.remainingElts.splice(insIndex, 0, elts[i]);
    }
}

htmlhider.HTMLHider.prototype.hideOneElement = function() {
    if (this.remainingElts.length == 0) {
        return false;
    }
    var eltToHide = this.remainingElts.pop();
    htmlhider.debugPrint("eltToHide = " + eltToHide);
    htmlhider.debugPrint("remLength = " + this.remainingElts.length);
    eltToHide.style.visibility = 'hidden';
    return true;
}

htmlhider.randomFromTo = function(from, to) {
    return Math.floor(Math.random() * (to - from + 1) + from);
}

htmlhider.debugPrint = function(str) {
    var elt = document.getElementById("debug");
    elt.innerHTML += str + "<br>";
}
