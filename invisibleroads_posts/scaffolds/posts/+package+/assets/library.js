!function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a="function"==typeof require&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}for(var i="function"==typeof require&&require,o=0;o<r.length;o++)s(r[o]);return s}({1:[function(require,module,exports){setTimeout(function(){"rgb(51, 51, 51)"!=$("body").css("color")&&$("head").append('<link rel="stylesheet" href="'+d.posts.assets_url+'/bootstrap/css/bootstrap.min.css"/>')},1e3)},{}],2:[function(require,module,exports){require("invisibleroads-posts"),window.setInterval(function(){$("#clock").text((new Date).getTime())},1e3)},{"invisibleroads-posts":1}]},{},[2]);
