var _fout_protocol  = (("https:" == document.location.protocol) ? "https://" : "http://");
var _fout_rtg_host  = 'cnt.fout.jp';
var _fout_beacon_host   = 'js.fout.jp';
var _fout_url = '';
var _fout_rurl = '';
var _fout_is_mobile = 0;

try {
    _fout_rurl = parent.document.referrer;
} catch (e){
    _fout_rurl = '';
}

try {
    _fout_url = parent.document.URL;
} catch (e){
    _fout_url = document.referrer;
}

_fout_is_mobile = fout_is_mobile_safari();

if (typeof(_fout_check) != "undefined") {
    _fout_check++;
} else {
    _fout_check=1;
}

if (typeof(_fout_userid)=="undefined") _fout_userid = '';
if (typeof(_fout_siteid)=="undefined") _fout_siteid = '';
if (typeof(_fout_segid)=="undefined") _fout_segid = '';
if (typeof(_fout_callback)=="undefined") _fout_callback = '';

var _is_cookie_mode = 0;

if (_fout_is_mobile == 1) {
    try{
        if (window.localStorage) {
            _is_cookie_mode = 0;
        } else {
            _is_cookie_mode = 1;
        }
    } catch (e) {
    }
} else {
    _is_cookie_mode = 1;
}

if (_fout_check < 5) {
    if (_is_cookie_mode == 1) {
        fout_cookie_targeting();
    } else {
        fout_mobile_targeting();
    }
}

(function beaconing() {
    var obj = document.createElement('iframe');
    obj.src = _fout_protocol + _fout_beacon_host + '/beacon.html';
    obj.style.display = 'none';
    fout_dom_ready(function() {
        document.body.appendChild(obj);
    });
})();

function fout_cookie_targeting() {
    if ( _fout_userid ) {
        var _fout_query = 'id=' + _fout_userid +
            '&url=' + encodeURIComponent(_fout_url) +
            '&rurl='  + encodeURIComponent(_fout_rurl) +
            '&siteid=' + _fout_siteid +
            '&segid=' + _fout_segid +
            '&bc=1';

        var _fout_src = _fout_protocol + _fout_rtg_host + "/" + _fout_userid + "/cnt?" + _fout_query;
        (new Image()).src = _fout_src;
    }
}

function fout_mobile_targeting() {
    if (_fout_userid) {
        var _fout_query = 'id=' + _fout_userid +
            '&url=' + encodeURIComponent(_fout_url) +
            '&rurl='  + encodeURIComponent(_fout_rurl) +
            '&siteid=' + _fout_siteid +
            '&segid=' + _fout_segid;

        var obj = document.createElement("iframe");
        obj.src = "https://dsp.fout.jp/js/sp_segmentation.html?" + _fout_query;
        obj.style.display = "none";
        fout_dom_ready(function() {
            document.body.appendChild(obj);
        });
    }
}

function fout_is_mobile_safari() {
    var useragents = [
        'iPhone', // Apple iPhone
        'iPod',   // Apple iPod touch
        'iPad'    // Apple iPad
    ];
    var pattern = new RegExp(useragents.join('|'),'i');
    return pattern.test(navigator.userAgent);
}

function fout_dom_ready(callback){
    var isLoaded = false;

    if (document.readyState === 'complete' || document.readyState === 'loaded') {
        callback();
        return;
    }

    if (document.addEventListener){
        document.addEventListener("DOMContentLoaded",function(){
            callback();
            isLoaded = true;
        }, false);
        window.addEventListener("load", function(){
            if (!isLoaded) callback();
        }, false);
    } else if (window.attachEvent) {
        if (window.ActiveXObject && window === window.top) {
            _ie();
        } else {
            window.attachEvent("onload", callback);
        }
    } else {
        var _onload = window.onload;
        window.onload = function(){
            if (typeof _onload === 'function') {
                _onload();
            }
            callback();
        }
    }
    function _ie(){
        try {
            document.documentElement.doScroll("left");
        } catch (e) {
            setTimeout(_ie, 0);
            return;
        }
        callback();
    }
}
