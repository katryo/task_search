/**
* DeqwasAgent
* デクワスで使用するjavascriptのための共通クラスである。
*/
//// Version 2.1.0

var DeqwasDebug = false;

DeqwasAgent = function () {
    this.initialize.apply(this, arguments);
};

//
// 定数定義
// 初期状態ではデフォルト値が入っていて、コンストラクタでdeqwas.constantをバインドする。
//
DeqwasAgent.domain = 'kdex001.deqwas.net';       // アプリケーションを運用するドメイン名
DeqwasAgent.appName = 'common';                   // アプリケーション名
DeqwasAgent.collectaspx = 'Collection.aspx';    // Collection.aspx
DeqwasAgent.choiceaspx = 'Choice.aspx';         // Collection.aspx
DeqwasAgent.CollectDivId = 'deqwas-collection-k'; 
// iframeを入れるデフォルトのdivタグのID（収集のみ）
DeqwasAgent.ScreenDivId = 'deqwas-screen-k';      // iframeを入れるデフォルトのdivタグのID（表示あり）
DeqwasAgent.urlLimitation = 2083;               // URLに使える半角文字数の最大値
DeqwasAgent.ScriptType = "rec";                 // レコメンド：rec、広告：ad
DeqwasAgent.urlmaxlength = 1024;                // 広告の際、URL、リファラーの最大文字数
DeqwasAgent.deqwasName = 'deqwas-k';
// iframeを入れるデフォルトのdivタグのID（収集のみ）

/**
 * スマートフォンかどうか判定
 */
DeqwasAgent.is_smartPhone = function () {
	var media = [
    'iPhone',
    'iPad',
    'Android',
    'blackberry',
    'windowsPhone'
    ];
    var pattern = new RegExp(media.join('|'), 'i');
    return pattern.test(navigator.userAgent);
};

/**
* URLパラメータを整理する
*/
DeqwasAgent.GetParamaterList = function () {
    if (DeqwasAgent.URLParamaters) { return DeqwasAgent.URLParamaters; }
    DeqwasAgent.URLParamaters = new Object();
    var ary = location.search.split(/[\?\&]/);
    for (var i = 0; i < ary.length; i++) {
        if (!ary[i] || !ary[i].match(/=+/)) { continue; }
        var pm = ary[i].split('=');
        DeqwasAgent.URLParamaters[pm[0]] = pm[1];
    }
    return DeqwasAgent.URLParamaters;
};

/**
* ベースとなるURLを取得
*/
DeqwasAgent.GetBaseUrl = function () {
    return (location.protocol == 'https:' ? 'https:' : 'http:') + '//' + DeqwasAgent.domain + '/' + DeqwasAgent.appName;
};

/**
* 配列の中にオブジェクトが存在するか
*/
DeqwasAgent.ArrayContains = function (array, obj) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
};

/**
* オブジェクトのクローンを作成する
* @objクローンするオブジェクト
*/
DeqwasAgent.Clone = function (obj) {
    var obj2 = new Object();
    for (var key in obj) {
        if (obj[key] == null) {
            obj2[key] = null;
        } else if (typeof obj[key] == "Array") {
            obj2[key] = new Array();
            for (var i = 0; i < obj[key].length; i++) {
                obj2[key].push(obj[key][i]);
            }
        } else if (typeof obj[key] == "Object") {
            obj2[key] = DeqwasAgent.Clone();
        } else {
            obj2[key] = obj[key];
        }
    }
    return obj2;
};

/**
* 文字を連結する
* @obj String 連結する複数の文字列
*/
DeqwasAgent.Concat = function (obj) {
    var txt = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        txt += arguments[i];
    }
    return txt;
};

/**
* 区切り文字を使用して文字を連結する
* @sep String 区切り文字
* @obj String 連結する複数の文字列
*/
DeqwasAgent.ConcatSep = function (sep, obj) {
    var s = '';
    var txt = arguments[1];
    for (var i = 2; i < arguments.length; i++) {
        txt += s;
        txt += arguments[i];
        s = sep;
    }
    return txt;
};

/**
* Deqwas.Collectでサポートしているもの
* この中に記述されているものは自動収集される。
* なお、SiteCatalyst以外はデフォルトで収集される。
*/
DeqwasAgent.CollectorConst = {
    Keywords: 1,
    Description: 2,
    SiteCatalyst: 4,
    Title: 8
};

//
// クッキー関連のライブラリ
//

/**
* ファーストパーティクッキーを取得する
* @key String クッキーのキー
*/
DeqwasAgent.GetCookie = function (key) {
    var cookieKey = key + "=";
    var val = null;
    var cookie = document.cookie + ";";
    var index = cookie.lastIndexOf(cookieKey);
    if (index != -1) {
        var endIndex = cookie.indexOf(";", index);
        val = unescape(cookie.substring(index + cookieKey.length, endIndex)) + ";";
    }
    return val;
};

/**
* ファーストパーティクッキーを設定する。
* なお、有効期限は１年間。
* @key String 設定するキー
* @val String 設定する値
*/
DeqwasAgent.SetCookie = function (key, val) {
    date = new Date();
    date.setTime(date.getTime(), (365 * 24 * 60 * 60 * 1000));
    myItem = DeqwasAgent.Concat(key, "=", escape(val), ";");
    myExpires = DeqwasAgent.Concat("expires=", date.toGMTString());
    document.cookie = DeqwasAgent.Concat(myItem, myExpires, "path=/");
};

/**
* ファーストパーティクッキーを削除する。
* @key String 削除するキー
*/
DeqwasAgent.DeleteCookie = function (key) {
    DeqwasAgent.SetCookie(key, '');
};

//
// クラスメソッド定義
//
DeqwasAgent.prototype = {
	codeVersion: 'xxx',
	collectionType: { normal: 'i', cart: 'c', shipping: 's' },
	screenType: { normal: 'r', cart: 'k', shipping: 'h' },
	screenElementId: DeqwasAgent.ScreenDivId,
	collectionElementId: DeqwasAgent.CollectDivId,
	visibleFunctionIds: { r: true, k: true, h: true },
	etccount: 0,

	/**
	* コンストラクタ
	* @site String サイトID
	* @role String データ収集の種別
	* @deqwasObject String デクワスの設定を代入しているオブジェクト
	*/
	initialize: function (site, role, deqwasObject) {
		// 定数バインド
		if (deqwasObject && deqwasObject.constant) {
			for (var key in deqwasObject.constant) {
				if (deqwasObject.constant[key])
					DeqwasAgent[key] = deqwasObject.constant[key];
			}
		}

		this.site = site;
		this.role = role;
		this.objectId = deqwasObject.id;
		if (deqwasObject.option == undefined) {
			deqwasObject.option = new Object();
		}

		this.silence = deqwasObject.option.silence;

		this.parameters = {
			cid: this.site,
			fc: "",
			iid: deqwasObject.id,
			role: this.role,
			iname: deqwasObject.name,
			l: deqwasObject.location,
			caption: deqwasObject.caption,
			expression: "",
			essential: "",
			uid: deqwasObject.viewer_id,
			image: deqwasObject.image,
			price: deqwasObject.price,
			category: deqwasObject.category,
			place: "",
			cb: (new Date()).getTime()
		};
		this.defCollect();

		this.parameterPriority = {
									higher: ['cid', 'fc', 'iid', 'type']
									,lower: []
								};

		this.noscreen = deqwasObject.option.noscreen;
		if (deqwasObject.option.noscreen || deqwasObject.option.solitude) {
			this.parameters.expression = deqwasObject.option.noscreen ? 'F' : 'X';
			this.parameters.expression += deqwasObject.option.solitude ? 'T' : 'X';
		}

		this.targetUrl = DeqwasAgent.GetBaseUrl() + "/" + DeqwasAgent.collectaspx;

		this.iframeStyle = {
			width: '0px',
			height: '0px'
		};
		this.iframeOptions = {
			frameBorder: "0",
			scrolling: "no"
		};
	},

	/**
	* データの有効制御を設定する。
	* @essential String データの有効制御
	*  NONE、nothging：essentialを利用しない。全て有効なデータになる。
	*  cofirmation：全て無効なデータとなる。
	*  minimum：アイテム名とid(ユーザIDかアイテムID）が無いものは無効データとなる。
	*  指定なし：アイテム名とid(ユーザIDかアイテムID）とリンクが無いものは無効データとなる。
	*/
	setEssential: function (essential) {
		this.parameters.essential = essential;
	},

	// パラメータ生成
	_createIframeSrcWithLimit: function (parameters, targetUrl) {
		var parameterArray = [];
		var dummies = new Object(); // for filtering entries coming from Object.prototype

		var parameterKeys = this._concatKey(this.parameterPriority, parameters);

		var iframeSrc = '' + targetUrl;
		var length = iframeSrc.length;
		for (var i = 0; i < parameterKeys.length; i++) {
			var key = parameterKeys[i];
			if (parameters[key] && typeof parameters[key] != 'function' && typeof dummies[key] == 'undefined') {
				var value = (typeof parameters[key] == 'string') ? parameters[key].replace(/[\f\n\r\t\v]/g, '') : parameters[key];
				var parameter = key + "=" + encodeURIComponent(value);
				length += 1 + parameter.length;
				if (length > DeqwasAgent.urlLimitation) {
					break;
				}
				parameterArray.push(parameter);
			}
		}
		iframeSrc += '?' + parameterArray.join("&");
		return iframeSrc;
	},

	// キーをつなげる
	_concatKey: function (keys, hash) {
		var array = [].concat(keys.higher, keys.lower);
		for (var key in hash) {
			if (!DeqwasAgent.ArrayContains(array, key)) {
				array.splice(array.length - keys.lower.length, 0, key);
			}
		}
		return array;
	},

	// CSS、optionなどを生成						
	_flatten: function (hash, assignment, terminator) {
		var txt = '';
		for (var key in hash) {
			txt += key;
			txt += assignment;
			txt += hash[key];
			txt += terminator;
		}
		return txt;
	},

	/**
	* サーバへと渡す追加パラメータを設定する。
	* @additionalParameters Object 追加パラメータのハッシュオブジェクト
	*/
	setAdditionalParameters: function (additionalParameters) {
		for (var key in additionalParameters) {
			this.parameters[key] = additionalParameters[key];
		}
	},

	/**
	* 表示するiframeを生成する場所を示すdivタグのidを設定する。
	* 基本的には、deqwas.constant.ScreenDivIdを使用し、この関数は使用しない。
	* @elementId String divタグのID
	*/
	setScreenElementId: function (elementId) {
		this.screenElementId = elementId;
	},

	/**
	* 収集するiframeを生成する場所を示すdivタグのidを設定する。
	* 基本的には、deqwas.constant.CollectionDivIdを使用し、この関数は使用しない。
	* @elementId String divタグのID
	*/
	setCollectionElementId: function (elementId) {
		this.collectionElementId = elementId;
	},

	/**
	* 生成するiframeのスタイルを設定する。
	* @width int iframeの幅(px)
	* @height int iframeの高さ(px)
	* @styleObject Object その他の設定のハッシュオブジェクト
	*/
	setIframeStyle: function (width, height, styleObject) {
		if (!width || !height) return;
		styleObject = styleObject || {};

		this.iframeStyle.width = width;
		this.iframeStyle.height = height;
		this.parameters["area"] = width + 'x' + height;
		for (var key in styleObject) {
			this.iframeStyle[key] = styleObject[key];
		}
	},

	/**
	* 生成するiframeのoptionを設定する。
	* @iframeOptions Object iframeのoptionに設定するハッシュオブジェクト
	*/
	setIframeOptions: function (iframeOptions) {
		if (!iframeOptions) return;
		for (var key in iframeOptions) {
			this.iframeOptions[key] = iframeOptions[key];
		}
	},

	// 最終的にiframeを生成し、エレメントを返す
	_createIframe: function (src, id, name, style, options) {
		var ifElem = document.createElement('iframe');
		ifElem.setAttribute('id', id);
		ifElem.setAttribute('src', src);
		ifElem.setAttribute('name', name);
		ifElem.setAttribute('style', this._flatten(style, ':', ';'));
		if (style.width) {
			ifElem.setAttribute('width', style.width);
		}
		if (style.height) {
			ifElem.setAttribute('height', style.height);
		}
		for (var key in options) {
			ifElem.setAttribute(key, options[key]);
		}
		if (DeqwasDebug) alert(src);
		return ifElem;
	},

	/**
	* iframeを生成し、対応するdivエレメント内に追加する。
	* @functionId String 行動履歴
	*  nomal:アイテムページをユーザが閲覧したとき。
	*  cart:アイテムをユーザがカートに入れたとき。
	*  shipping:アイテムをユーザが購入(コンバージョン)したとき。
	* @isCollectOnly bool レコメンドを表示するか
	*/
	appendIframeToElement: function (functionId, isCollectOnly) {
		var elementId;
		var functionCode;
		// functionIdを一文字の表示IDに変換
		if (isCollectOnly) {
			functionCode = this.collectionType[functionId]; // 収集のみの時
			elementId = this.collectionElementId;
		} else {
			functionCode = this.screenType[functionId]; // 表示する時
			elementId = this.screenElementId;
		}
		// パラメータにファンクションID設定
		this.parameters.fc = functionCode;

		// Div要素がないときは作成する
		if (!document.getElementById(elementId)) {
			var divElem = document.createElement('div');
			divElem.setAttribute('id', elementId);
			document.body.appendChild(divElem);
		}
		// silenceの時は無条件で無効データフラグ
		if (this.silence) {
			this.parameters.essential = 'confirmation';
		}
		// 表示しないフラグが立っているとき
		if (this.noscreen) {
			this.iframeStyle = { width: '0px', height: '0px' };
		}

		//
		// ここからiframe生成処理
		//

		// 表示するとき
		if (this.visibleFunctionIds[functionCode]) {
			elementId = this.screenElementId;
		}
		// 表示しない時
		else {
			elementId = this.collectionElementId;
			this.iframeStyle = { width: '0px', height: '0px' };
		}
		var deqwasName = DeqwasAgent.deqwasName + '_' + functionId;
		if (!document.getElementById(deqwasName)) {
			document.getElementById(elementId).appendChild(
                this._createIframe(
                    this._createIframeSrcWithLimit(this.parameters, this.targetUrl),
                    deqwasName,
                    deqwasName,
                    this.iframeStyle,
                    this.iframeOptions));
		}
		return deqwasName;
	},

	/**
	* 既定の情報収集。コンストラクタ内で使用されるため、基本的に使用しない。
	*/
	defCollect: function () {
		// 広告の場合
		// トップフレームを取得
		var topwin = window;
		//        while (topwin.parent != undefined && topwin.parent != null && topwin.parent != topwin) {
		//            topwin = topwin.parent;
		//        }

		// Location
		if (topwin.document && topwin.document.location) {
			var url = topwin.document.location.href;
			if (url.length > DeqwasAgent.urlmaxlength) {
				url = url.substring(0, DeqwasAgent.urlmaxlength);
				this.parameters['url_flg'] = '1';
			} else {
				this.parameters['url_flg'] = '0';
			}
			this.parameters['url'] = url;
		}
		// Referrer
		if (topwin.document && topwin.document.referrer) {
			var ref = topwin.document.referrer;
			if (ref.length > DeqwasAgent.refmaxlength) {
				ref = ref.substring(0, DeqwasAgent.refmaxlength);
				this.parameters['ref_flg'] = '1';
			} else {
				this.parameters['ref_flg'] = '0';
			}
			this.parameters['ref'] = ref;
		}

		// deqwas_inflow
		var deqwas_inflow = DeqwasAgent.GetParamaterList()["deqwas_inflow"];
		if (deqwas_inflow) {
			this.parameters['inflow'] = deqwas_inflow;
		}

		this.collect(
            DeqwasAgent.CollectorConst.Keywords,
            DeqwasAgent.CollectorConst.Description,
            DeqwasAgent.CollectorConst.Title);
	},

	/**
	* 情報収集。DeqwasAgent.CollectorConstに記述されているものがサポートされる。
	* @flg int 収集する情報を、DeqwasAgent.CollectorConstを"|"（or）区切りで記述。
	*/
	collect: function () {
		// 引数をフラグに直す
		var flg = 0;
		for (var i = 0; i < arguments.length; i++) {
			flg |= arguments[i];
		}
		// 先にmetaタグから収集関連ものをやる
		var metas = document.getElementsByTagName("meta");
		for (var i = 0; i < metas.length; i++) {
			var meta = metas[i];
			var name = meta.getAttribute('name');
			var equiv = meta.getAttribute('http-equiv');
			var content = meta.getAttribute('content');
			if (!name || !content) continue;
			// キーワード
			if ((DeqwasAgent.CollectorConst.Keywords & flg) == DeqwasAgent.CollectorConst.Keywords) {
				if (name.match(/keywords/i)) {
					this.parameters['keywords'] = content;
				}
			}
			// description
			if ((DeqwasAgent.CollectorConst.Description & flg) == DeqwasAgent.CollectorConst.Description) {
				if (name.match(/description/i)) {
					this.parameters['description'] = content;
				}
			}
		}

		// トップフレームを取得
		var mywin = window;
		//        while (mywin.parent != undefined && mywin.parent != null && mywin.parent != mywin) {
		//            mywin = mywin.parent;
		//        }
		var topwin = mywin;
		// Title
		if ((DeqwasAgent.CollectorConst.Title & flg) == DeqwasAgent.CollectorConst.Title) {
			this.parameters['title'] = topwin.document.title;
		}

		// サイトカタリスト取得。サイトカタリストはライブラリがない場合機能しない。
		// サイトカタリストは、直接paramatersにはセットせず、
		// 一旦DeqwasAgentインスタンスのcatalystsにハッシュがセットされる。
		if ((DeqwasAgent.CollectorConst.SiteCatalyst & flg) == DeqwasAgent.CollectorConst.SiteCatalyst) {
			var catalysts = {};
			if (typeof window.s === 'object') {
				var variables = window.s.vl_g.split(',');
				for (var i in variables) {
					if (typeof variables[i] === 'string') {
						var name = variables[i];
						var type = window.s[name] ? typeof window.s[name] : typeof window.s[name.toLowerCase()];
						if (type === 'string' || type === 'number' || type === 'boolean') {
							catalysts['s_' + name.toLowerCase()] = window.s[name];
						}
					}
				}
			}
			this.catalysts = catalysts;
		}
	},

	/**
	* 行動付加情報。note0～note9に入る値を設定。入りきらない場合は、etcに入る。
	* @arg Object 可変長引数。設定する順番に引数に記述する。
	*/
	SetActOption: function () {
		for (var i = 0; i < arguments.length; i++) {
			if (i < 10) {
				this.paramater["note" + i] = arguments[i];
			} else if (this.etccount < 10) {
				this.paramater["etc" + this.etccount] = arguments[i];
				this.etccount++;
			} else {
				return; // extraもetcもいっぱいになった時
			}
		}
	},

	/**
	* アイテム付加情報。extra0～extra9に入る値を設定。入りきらない場合は、etcに入る。
	* @arg Object 可変長引数。設定する順番に引数に記述する。
	*/
	SetItemOption: function () {
		for (var i = 0; i < arguments.length; i++) {
			if (i < 10) {
				this.paramater["extra" + i] = arguments[i];
			} else if (this.etccount < 10) {
				this.paramater["etc" + this.etccount] = arguments[i];
				this.etccount++;
			} else {
				return; // extraもetcもいっぱいになった時
			}
		}
	}
};

if (window.DeqwasCallBack) window.DeqwasCallBack();

/**
 * 一つのページに複数のタグが設置されている場合の対応。
 * DeqwasCallBackを配列DeqwasCallBacksに* 格納し、
 * それを順次実行するように変更。
 */
if (window.DeqwasCallBacks) {
	for	(var cb in window.DeqwasCallBacks) {
		window.DeqwasCallBacks[cb]();
	}
} 
