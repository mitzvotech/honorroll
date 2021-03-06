/*******************************************************************************************
 * autoComplt
 *
 * Copyright (C) 2013 Fischer Liu | MIT license | https://github.com/Fischer-L/autoComplt.js
 -------------------------------------------------------------------------------------------
 *** Public APIs ***

	[ autoComplt ]
	> enable : function (input, params)
		# Func : Enable the autocomplete function on one <input> elem
		# Arg:
			<ELM> input = the <input> to enable
			<OBJ> params = { // optional. The obj holding settings to init the autocomplete, including
					 > hintsFetcher : refer to input.autoComplt.setHintsFetcher for the valid value
					 > delay, maxHintNum : refer to input.autoComplt.config for the valid value
				  }
		# Return:
			@ OK: <ELM> the <input>
			@ NG: null


	[ input.autoComplt ]
	After enabling, the <input> would be attached one autoComplt obj. Use the autoComplt obj to control the autocomplete function
	> setHintsFetcher = function (hintsFetcher)
		# Func : Setup the callback to fetch the autocomplete hint.
		# Arg:
			<FN> hintsFetcher = while user inputs sth, this hintsFetcher function would be invoked with 2 args.
			                   The 1st one is the user's input value(text). Please go fetching your autocomplete hints based the user's value
							   The 2nd one is one callback. Calling this callback would open the autocomplete list. This callback MUST be passed in the array of the hint texts or nothing happens.
							   So after fetching your autocomplete hints please call the 2nd arg callback to open the autocomplete list.
							   If the hintsFetcher function is not set, no autocomplete funciton works.
		# Return:
			@ OK: true
			@ NG: false
	> config = function (params)
		# Func : Config the autocomplete funciton and the styles
		# Arg:
			<OBJ> params = {
					<NUM> delay : the ms delays the work of fetching the autocomplete hints based on the user's input. Default is 100.
					<NUM> maxHintNum : the max number of hints displayed. Default is 10
				  }
		# Return:
			@ OK: <OBJ> An obj carrying the configs which just has been changed during the call. You could use it to check out whether the config action is successful or not
			@ NG: false
	> setStyle = function (targetClass, styles)
		# Func : Set the autocomplete list's ui styles
		# Arg:
			<STR> targetClass = the css class selector of the target ui part which is being set styles, the valid value could be:
			                    "autoComplt-list" => the autocomplete ul list
								"autoComplt-hint" => the autocomplete hints
								"autoComplt-hint-selected" => the autocomplete hint selected
			<OBJ> styles = { // The obj holding the new styles to set
						// For "autoComplt-list", the style which could be set
						> "border", "maxHeight", "backgroundColor" : refer to the valid CSS values
						
						// For "autoComplt-hint", the style which could be set
						> "height", "padding", "margin", "color", "backgroundColor", "fontSize" : refer to the valid CSS values
						
						// For "autoComplt-hint-selected", the style which could be set
						> "color", "backgroundColor" : refer to the valid CSS values
				  }
		# Return: 
			@ OK: <OBJ> An obj carrying the new styles' value which just has been set during the call. 
			@ NG: false
	> close = function ()
		# Func : Close the autocomplete list
		# Return: n/a
	> enable = function ()
		# Func : Enable the autocomplete function
		# Return: n/a
	> disable = function ()
		# Func : Disable the autocomplete function
		# Return: n/a
	> destroy = function ()
		# Func : Destroy the autocomplete function. Unlike this.disable which could be enabled again, this is going to eliminate all the functions.
		# Return: n/a
*******************************************************************************************/
var autoComplt = (function () {
/*	Properties:
		[ Private ]
		<OBJ> _CONST = the constants collection
		<OBJ> _ui = the obj to build UI
		<CLS> _AutoCompltList = the class dealing with the autocomplete operations
		[ Public ]
		> Refer to the Public APIs above
	Methods:
		[ Private ]
		> _normalizeEvt : Normalize the event obj
		> _addEvt : Add an event to one elem, used for cross-browser mitigation
		> _rmEvent : remove an event to one elem, used for cross-browser mitigation
		> _getComputedStyle : Get the computed style value, used for cross-browser mitigation
		[ Public ]
		> enable : Refer to the Public APIs above
		
*/
	var _DBG = 0; // A little debug flag
	
	var _CONST = {
		
		autoCompltListClass : "autoComplt-list",
		
		autoCompltHintClass : "autoComplt-hint",
		
		autoCompltHintSelectedClass : "autoComplt-hint-selected",
		
		maxHintNum : 10,
		
		autoCompltDelay : 100, // in ms
		
		listStatus : {
			attr : "data-listStatus",
			open : "open",
		},
		
		keyCode : {
			up : 38,
			down : 40,
			esc : 27,
			enter : 13
		},
	
		defaultStyles : {
		
			autoCompltList : {
				maxHeight : "none",
				border : "1px solid #aaa",
				padding : "0",
				margin: "0",
				zIndex : 99,
				overflowX : "hidden",
				overflowY : "auto",
				display : "none",
				position: "absolute",
				backgroundColor : "#fff",
			},
			
			autoCompltHint : {
				height : "1.5em",
				padding: "2px 6px 2px 10px",
				margin: "6px 0",
				overflow: "hidden",
				listStyleType: "none",
				color : "#000",
				backgroundColor : "#fff",
				cursor : "default",
				fontSize : "1em"
			},
			
			autoCompltHintSelected : {
				color : "#fff",
				backgroundColor : "#3399ff"
			}
		},
		
		adjStyleAttrs : {
			autoCompltList : [ "border", "maxHeight", "backgroundColor" ],
			autoCompltHint : [ "height", "padding", "margin", "color", "backgroundColor", "fontSize" ],
			autoCompltHintSelected : [ "color", "backgroundColor" ]
		}
	};
	/*	Arg:
			<OBJ> e = the event obj
		Return:
			<OBJ> the normalized event obj
	*/
	var _normalizeEvt = function (e) {					
		e = e || window.event;
		e.target = e.target || e.srcElement;
		e.stopBubble = function () {
			this.cancelBubble = true;
			if (this.stopPropoagation) { this.stopPropoagation(); }
		}
		e.stopDefault = function () {
			if (this.preventDefault) { this.preventDefault(); }
			this.returnValue = false;
			return false;
		}
		return e;
	}
	/*	Arg:
			<ELM> elem = the DOM elem
			<STR> evt = the event name
			<FN> eHandle = the event handle
	*/
	var _addEvt = function (elem, evt, eHandle) {
		if (elem.addEventListener) {
			elem.addEventListener(evt, eHandle);
		} else if (elem.attachEvent) { // The IE 8 case
			elem.attachEvent("on" + evt, eHandle);
		}
	}
	/*	Arg: Refer to _addEvt
	*/
	var _rmEvent = function (elem, evt, eHandle) {
		if (elem.removeEventListener) {
			elem.removeEventListener(evt, eHandle);
		} else if (elem.detachEvent) { // The IE 8 case
			elem.detachEvent("on" + evt, eHandle);
		}
	}
	/*	Arg:
			<ELM> elem = the DOM elem
			<STR> name = the style name
	*/
	var _getComputedStyle = function (elem, name) {
		var v = null;
		
		if (window.getComputedStyle) {
			
			v = window.getComputedStyle(elem)[name] || null;
			
		} else if (elem.currentStyle) { // Hack for IE...Reference from the jQuery
			
			v = elem.currentStyle && elem.currentStyle[name]
			
			var left,
				rsLeft,
				style = elem.style;

			// Avoid setting v to empty string here
			// so we don't default to auto
			if ( v == null && style && style[name] ) {
				v = style[ name ];
			}

			// From the awesome hack by Dean Edwards
			// http://erik.eae.net/archives/2007/07/27/18.54.15/#comment-102291

			// If we're not dealing with a regular pixel number
			// but a number that has a weird ending, we need to convert it to pixels
			// but not position css attributes, as those are proportional to the parent element instead
			// and we can't measure the parent instead because it might trigger a "stacking dolls" problem

			// Remember the original values
			left = style.left;
			rsLeft = elem.runtimeStyle && elem.runtimeStyle.left;

			// Put in the new values to get a computed value out
			if ( rsLeft ) {
				elem.runtimeStyle.left = elem.currentStyle.left;
			}
			style.left = name === "fontSize" ? "1em" : v;
			v = style.pixelLeft + "px";

			// Revert the changed values
			style.left = left;
			if ( rsLeft ) {
				elem.runtimeStyle.left = rsLeft;
			}
			
		}
		
		return v;
	}
	/*	Methods:
			[ Public ]
			> buildElem : Build on elem from the HTML text
			> buildHint : Build one autocomplete hint elem
			> buildList : Build one autocomplete list
	*/
	var _ui = {
		/*	Arg:
				<STR> html = the HTMl text
			Return:
				<ELM> the elem built from the input HTML
		*/
		buildElem : function (html) {
			var div = document.createElement("DIV");
			div.innerHTML = html;
			return div.firstChild.cloneNode(true);
		},
		/*	Arg:
				<STR> hint = the hint text
				<OBJ> styles = the obk holding the styles to set. Refer to _CONST.defaultStyles.autoCompltHint for the required styles
			Return:
				@ OK: <ELM> the hint ui elem
				@ NG: null
		*/
		buildHint : function (hint, styles) {
			if (typeof hint == "string" && hint) {
				var hint = this.buildElem('<li class="' + _CONST.autoCompltHintClass + '">' + hint + '</li>');

				hint.style.height = hint.style.lineHeight = styles.autoCompltHint.height; // line-height shall always be equal to the height
				hint.style.padding = styles.autoCompltHint.padding;
				hint.style.margin = styles.autoCompltHint.margin;
				hint.style.overflow = styles.autoCompltHint.overflow;
				hint.style.listStyleType = styles.autoCompltHint.listStyleType;
				hint.style.color = styles.autoCompltHint.color;
				hint.style.backgroundColor = styles.autoCompltHint.backgroundColor;
				hint.style.cursor = styles.autoCompltHint.cursor;
				hint.style.fontSize = styles.autoCompltHint.fontSize;

				return hint;
			}
			return null;
		},				
		/*	Arg:
				<OBJ> styles = the obk holding the styles to set. Refer to _CONST.defaultStyles.autoCompltList for the required styles
			Return:
				@ OK: <ELM> the list ui elem
				@ NG: null
		*/
		buildList : function (styles) {
			var list = this.buildElem('<ul class="' + _CONST.autoCompltListClass + '"></ul>');
			
			list.style.maxHeight = styles.autoCompltList.maxHeight;
			list.style.border = styles.autoCompltList.border;	
			list.style.padding = styles.autoCompltList.padding;
			list.style.margin = styles.autoCompltList.margin;
			list.style.zIndex = styles.autoCompltList.zIndex;
			list.style.overflowX = styles.autoCompltList.overflowX;
			list.style.overflowY= styles.autoCompltList.overflowY;
			list.style.display = styles.autoCompltList.display;
			list.style.position = styles.autoCompltList.position;
			list.style.backgroundColor = styles.autoCompltList.backgroundColor;

			return list;
		}
	};
	/*	Properties:
			[ Public ]
			<ELM> uiElem = the autocomplete list current being displayed and associated with.
			<ELM> assocInput = the input elem associated with
			<BOO> mouseOnList = A little flag marking the moused is on the top of the autocomplete list
			<NUM> maxHintNum = The max number of hints displayed
			<OBJ> styles = the obj holding the style setting of the list and hints. Refer to _CONST.defaultStyles for the required styles.
		Methods:
			[ Public ]
			> genList : Build and setup one autocomplete list
			> isHint : Check if it is a autocomplete hint elem or not
			> putHints : Put hints into the autocomplete list
			> clearHints : Clear all hints
			> isOpen : Tell if the auotcomplete list is open or not
			> open : Open the autocomplete list. NOTICE: before opening, there must at one hint in the list so please call this.putHints first then open.
			> close : Close the autocomplete list
			> autoScroll : Auto scroll the list according the position and offset of the current selected hint so the current selected hint could show up
			> select : Selece one hint. NOTICE: this action will not change this.assocInput's value. Please use this.getSelected to get the selected hint and extract the hint text and assign this.assocInput's value the hint text
			> deselect : Deselect all hints
			> getSelected : Get the hint elem selected
	*/
	var _AutoCompltList = function (assocInput) {

		this.uiElem = null;
		this.assocInput = assocInput;
		this.mouseOnList = false;
		this.pauseMouseoverSelection = false;
		this.pauseMouseoutDeselection = false;
		this.maxHintNum = _CONST.maxHintNum;
		this.styles = JSON.parse(JSON.stringify(_CONST.defaultStyles)); // Copy the default first

	}; {
		/*
		*/
		_AutoCompltList.prototype.genList = function () {
			if (!this.uiElem) {
			
				var that = this;
				
				this.uiElem = _ui.buildList(this.styles);						
				
				// Make hint selected onmouseover
				_addEvt(this.uiElem, "mouseover", function (e) {
					e = _normalizeEvt(e);
					if (that.isHint(e.target)) {
						that.select(e.target);
						that.autoScroll();
					}
				});
				
				// Make hint not selected onmouseout
				_addEvt(this.uiElem, "mouseout", function (e) {					
					e = _normalizeEvt(e);
					that.deselect();
				});
				
				// Prepare for the hint selection by clicking
				_addEvt(this.uiElem, "mousedown", function (e) {
					e = _normalizeEvt(e);	
					that.mouseOnList = true;						
					// One hack for FF.
					// Even call focus methos on the input's onblur event, however, still the input losese its focus.
					// As a result we have to set a timeout here
					setTimeout(function () {
						that.assocInput.focus();
					}, 50);
				});				
				
				// Select hint by clicking
				_addEvt(this.uiElem, "mouseup", function (e) {
					e = _normalizeEvt(e);
					if (that.isHint(e.target)) {
						that.select(e.target);
						that.assocInput.value = that.getSelected().innerHTML;
						that.assocInput.autoComplt.close();
					}
				});
				
				document.body.appendChild(this.uiElem);
			}
		}
		/*	Arg:
				<ELM> el = the elem to check
			Return:
				@ Ok: true
				@ NG: false
		*/
		_AutoCompltList.prototype.isHint = function (el) {
			if (el && typeof el == "object" && el.nodeType === 1) {
				var cls = " " + el.className + " ";
				return (cls.indexOf(" " + _CONST.autoCompltHintClass + " ") >= 0);
			}
			return false;
		}
		/*	Arg:
				<ARR> hints = the array of hint texts
			Return:
				<NUM> the number of hints put
		*/
		_AutoCompltList.prototype.putHints = function (hints) {
			var count = 0;
			if (hints instanceof Array) {
				var i,
					j,
					hs = [];
				
				j = Math.min(hints.length, this.maxHintNum);				
				for (i = 0; i < j; i++) {
					hs.push(_ui.buildHint(hints[i], this.styles));
					if (!hs[hs.length - 1]) {
						hs.pop();
					}
				}
				
				if (hs.length > 0) {
					var buf = document.createDocumentFragment();
					for (i = 0, count = hs.length; i < count; i++) {
						buf.appendChild(hs[i]);
					}
					this.clearHints();
					
					this.genList(); // Geneate the list in case there is none
					this.uiElem.appendChild(buf);							
				}
			}
			return count;
		}
		/*
		*/
		_AutoCompltList.prototype.clearHints = function () {
			if (this.uiElem) {
				this.uiElem.innerHTML = "";
			}
		}
		/*
			Return:
				@ Ok: true
				@ NG: false
		*/		
		_AutoCompltList.prototype.isOpen = function () {
			if (this.uiElem) {
				return (this.uiElem.getAttribute(_CONST.listStatus.attr) == _CONST.listStatus.open);
			}
			return false;
		}
		/*
		*/
		_AutoCompltList.prototype.open = function () {	
			var hints;
				
			if (this.uiElem
				&& (hints = this.uiElem.querySelectorAll("." + _CONST.autoCompltHintClass))
				&& hints.length // At lease one hint exists, we would open...
			) {
				var i,
					buf;
				
				// Position the list
				buf = this.assocInput.getBoundingClientRect();
				this.uiElem.style.top = (document.documentElement && document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop)
									  + buf.bottom + "px";
				this.uiElem.style.left = buf.left + "px";
				
				// Calculate the list's width
				buf = buf.right - buf.left - parseFloat(_getComputedStyle(this.uiElem, "borderLeftWidth")) - parseFloat(_getComputedStyle(this.uiElem, "borderRightWidth"));
				this.uiElem.style.width = buf + "px";

				// Calculate the list's height
				for (i = 0, buf = 0; i < hints.length; i++) {
					buf += parseFloat(_getComputedStyle(hints[i], "height"))
					     + parseFloat(_getComputedStyle(hints[i], "paddingTop"))
					     + parseFloat(_getComputedStyle(hints[i], "paddingBottom"));						 
						 
					if (hints[i+1]) { // Compute the margin between the hints
						buf += Math.max(
							parseFloat(_getComputedStyle(hints[i], "marginBottom")), parseFloat(_getComputedStyle(hints[i+1], "marginTop"))
						);
					}
				}
				buf += parseFloat(_getComputedStyle(hints[0], "marginTop"))
					 + parseFloat(_getComputedStyle(hints[hints.length - 1], "marginBottom"));
				this.uiElem.style.height = (buf + 1) + "px"; // Plus one for a little buffer

				// Open
				this.uiElem.setAttribute(_CONST.listStatus.attr, _CONST.listStatus.open);				
				this.uiElem.style.display = "block";
			}
		}
		/*
		*/
		_AutoCompltList.prototype.close = function () {
			if (this.uiElem && !_DBG) {
				this.mouseOnList = false;
				this.uiElem.parentNode.removeChild(this.uiElem);
				this.uiElem = null;
			}
		}
		/*
		*/
		_AutoCompltList.prototype.autoScroll = function () {
			var hint = this.getSelected();
			if (hint) {
				var currHint,
					offset = 0,
					minDisplayH = 0,
					hintH = hint.clientHeight,
					hintMT = parseFloat(_getComputedStyle(hint, "marginTop")),
					hintMB = parseFloat(_getComputedStyle(hint, "marginBottom"));
				
				currHint = hint.previousSibling;

				minDisplayH = hintH + (currHint ? Math.max(hintMT, hintMB) : hintMT); // The min height to display one hint
				
				while (currHint) {
				
					offset += hintH; // Add the current hint' hintH
					
					currHint = currHint.previousSibling;
					if (currHint) {
						// There is one hint before the current hint so calculate based on the collapsed model
						offset += Math.max(hintMT, hintMB);
					} else {
						// No more previous hint, this is the 1st hint so just take the marign top
						offset += hintMT;
					}
				}
				
				if (this.uiElem.clientHeight + this.uiElem.scrollTop - offset < minDisplayH
					|| offset - this.uiElem.scrollTop < minDisplayH
				) {
				// Ther is no enough room displaying the current selected hint so adjust the scroll
					this.uiElem.scrollTop = offset;
				}
			}
		}
		/*	Arg:
				<ELM|NUM> candidate = could be
				                      1) the hint elem or
									  2) the index of the hint in the list. Passing in -1 would select the last hint. Passing in 0 would select the 1st hint.
		*/
		_AutoCompltList.prototype.select = function (candidate) {
		
			if (this.uiElem) {
			
				var hint = null;
			
				if (this.isHint(candidate)) {
				
					hint = candidate;
				
				} else if (typeof candidate == "number" && (candidate >= 0 || candidate === -1)) {
				
					var hints = this.uiElem.querySelectorAll("." + _CONST.autoCompltHintClass);
					
					if (hints.length > 0) {
						hint = +candidate;
						hint = (hint === -1 || hint > hints.length - 1) ? hints.length - 1 : hint;
						hint = hints[hint];
					}					
				}
			
				if (hint !== null) {
					
					this.deselect();					
					hint.className += " " + _CONST.autoCompltHintSelectedClass;
					hint.style.color = this.styles.autoCompltHintSelected.color;
					hint.style.backgroundColor = this.styles.autoCompltHintSelected.backgroundColor;					
				}
			}
		}
		/*
		*/
		_AutoCompltList.prototype.deselect = function () {
			if (this.uiElem) {
				var slct = this.getSelected();
				if (slct) {
					slct.className = _CONST.autoCompltHintClass;
					slct.style.color = this.styles.autoCompltHint.color;
					slct.style.backgroundColor = this.styles.autoCompltHint.backgroundColor;
				}
			}
		}
		/*	Return:
				@ OK: <ELM> the selected hint element
				@ NG: null
		*/
		_AutoCompltList.prototype.getSelected = function () {
			return !this.uiElem ? null : this.uiElem.querySelector("." + _CONST.autoCompltHintSelectedClass) || null;
		}
	}

	var publicProps = {
		enable : function (input, params) {
			if (   input
				&& typeof input == "object"
				&& typeof input.tagName == "string"
				&& input.tagName.toLowerCase() == "input"
				&& input.type == "text"
				&& input.nodeType === 1
				&& !input.autoComplt
			) {
				
				/*	Propertise:
						[ Private ]
						<NUM> input_autoComplt_delay = the ms delays the work of fetching the autocomplete hints based on the user's input
						<BOO> input_autoComplt_enabled = true to perform the autocomplete function; false not to perform.
						<STR> input_autoComplt_currentTarget = the current user's input for which the autocomplete is target
						<OBJ> input_autoComplt_list = the instance of _AutoCompltList
					Methods:
						[ Private ]
						> input_autoComplt_hintsFetcher : The function fetching the autocomplete hints
						> input_autoComplt_startFetcher : Setup and call input_autoComplt_hintsFetcher to fetch the hints
						> input_autoComplt_compltInput : Autocomplete the <input> according to the hint selection state
						> input_autoComplt_blurEvtHandle, input_autoComplt_keyEvtHandle : The event handle
						[ Public ]
						> setHintsFetcher, config, setStyles, close, enable, disable, destroy : Refe to the Public APIs above
				*/
				input.autoComplt = {};
				
				var input_autoComplt_delay = _CONST.autoCompltDelay,
					input_autoComplt_enabled = true,
					input_autoComplt_currentTarget = "",
					input_autoComplt_hintsFetcher = null,
					input_autoComplt_list = new _AutoCompltList(input),
					/*
					*/
					input_autoComplt_startFetcher = function () {
						if (this.value.length > 0
							&& input_autoComplt_enabled
							&& typeof input_autoComplt_hintsFetcher == "function"
							&& input_autoComplt_currentTarget !== this.value // If equals, it means we've already been searching for the hints for the same value
						) {
							var fetcherCaller = {};
							
							fetcherCaller.call = function () {
								input_autoComplt_hintsFetcher.call(
									fetcherCaller.that,
									fetcherCaller.compltTarget,
									fetcherCaller.openHint
								);
							};
							
							fetcherCaller.that = input;
							
							// Record the autocomplete target for this fetching job
							fetcherCaller.compltTarget = input_autoComplt_currentTarget = this.value;
							
							fetcherCaller.openHint = function (hints) {
								// If the user's input has changed during the fetching, this fetching job is useless.
								// So only when the user's input doesn't change, we will proceed further.
								if (fetcherCaller.compltTarget === input_autoComplt_currentTarget) {							
									if (input_autoComplt_list.putHints(hints)) {
										input_autoComplt_list.open();
									} else {
										fetcherCaller.that.autoComplt.close();
									}
								}
							}
							
							setTimeout(fetcherCaller.call, input_autoComplt_delay);
						}
					},
					/*
					*/
					input_autoComplt_compltInput= function () {
						if (input_autoComplt_enabled) {
							var hint = input_autoComplt_list.getSelected();
							if (hint) {
								this.value = hint.innerHTML;
							} else {
							// If no hint is selected, just use the original user input to autocomplete
								this.value = input_autoComplt_currentTarget;
							}
						}
					},
					/*
					*/
					input_autoComplt_blurEvtHandle = function (e) {
						e = _normalizeEvt(e);
						if (input_autoComplt_list.mouseOnList) {
						// If the mouse is on the autocomplete list, do not close the list
						// and still need to focus on the input.
							input.focus();
							input_autoComplt_list.mouseOnList = false; // Assign false for the next detection
						} else {
							input.autoComplt.close();
						}
					},
					/*
					*/
					input_autoComplt_keyEvtHandle = function (e) {
						e = _normalizeEvt(e);
						if (input_autoComplt_enabled) {
							
							if (e.type == "keydown"
								&& input_autoComplt_list.isOpen()
								&& (e.keyCode === _CONST.keyCode.up || e.keyCode === _CONST.keyCode.down)
							) {
							// At the case that the hint list is open ans user is walkin thru the hints.
							// Let's try to autocomplete the input by the selected input.
								
								var hint = input_autoComplt_list.getSelected();
								
								if (e.keyCode === _CONST.keyCode.up) {
								
									if (!hint) {
									// If none is selected, then select the last hint
										input_autoComplt_list.select(-1);												
									} else if (hint.previousSibling) {
									// If some hint is selected and the previous hint exists, then select the previous hint
										input_autoComplt_list.select(hint.previousSibling);
									} else {
									// If some hint is selected but the previous hint doesn't exists, then deselect all
										input_autoComplt_list.deselect();
									}
									
								} else if (e.keyCode === _CONST.keyCode.down) {
								
									if (!hint) {
									// If none is selected, then select the first hint
										input_autoComplt_list.select(0);												
									} else if (hint.nextSibling) {
									// If some hint is selected and the next hint exists, then select the next hint
										input_autoComplt_list.select(hint.nextSibling);
									} else {
									// If some hint is selected but the next hint doesn't exists, then deselect all
										input_autoComplt_list.deselect();
									}
									
								}
								
								input_autoComplt_list.autoScroll();
								
								input_autoComplt_compltInput.call(input);

							}
							else if (e.type == "keyup") {
								
								var startFetching = false;
								
								switch (e.keyCode) {
									case _CONST.keyCode.up: case _CONST.keyCode.down:
										if (input_autoComplt_list.isOpen()) {
											// We have handled this 2 key codes onkeydown, so must do nothing here
										} else {
											startFetching = true;
										}
									break;
									
									case _CONST.keyCode.esc:
										if (input_autoComplt_list.isOpen()) {
											// When pressing the ESC key, let's resume back to the original user input
											input.value = input_autoComplt_currentTarget;
											input.autoComplt.close();
										}										
									break;
									
									case _CONST.keyCode.enter:
										if (input_autoComplt_list.isOpen()) {
											// When pressing the enter key, let's try autocomplete
											input_autoComplt_compltInput.call(input);
											input.autoComplt.close();
										}
									break;
									
									default:
										startFetching = true;
									break;
								}
								
								if (startFetching) {
									if (input.value.length > 0) {
										input_autoComplt_startFetcher.call(input);
									} else {
										input.autoComplt.close();
									}
								}
							}
						}
					};

				input.autoComplt.setHintsFetcher = function (hintsFetcher) {
					if (typeof hintsFetcher == "function") {
						input_autoComplt_hintsFetcher = hintsFetcher;
						return true;
					}
					return false;
				}
				
				input.autoComplt.config = function (params) {
					if (params instanceof Object) {
						
						var buf,
							pms = {};
						
						// Config the fetching delay timing
						//
						buf = Math.floor(params.delay);
						if (buf > 0) {
							input_autoComplt_delay = pms.delay = buf;
						}
						
						// Config the max number of displayed hints
						//
						buf = Math.floor(params.maxHintNum);
						if (buf > 0) {
							input_autoComplt_list.maxHintNum = pms.maxHintNum = buf;
						}
						
						return pms;
					}
					return false;
				}
				
				input.autoComplt.setStyles = function (targetClass, styles) {				
				
					var tStyles,
						adjStyleAttrs,
						newStyles = false;
					
					// Let's find out which the target UI part is being set
					switch (targetClass) {
						case _CONST.autoCompltListClass:
							tStyles = input_autoComplt_list.styles.autoCompltList;
							adjStyleAttrs = _CONST.adjStyleAttrs.autoCompltList;
						break;
						
						case _CONST.autoCompltHintClass:
							tStyles = input_autoComplt_list.styles.autoCompltHint;
							adjStyleAttrs = _CONST.adjStyleAttrs.autoCompltHint;
						break;
						
						case _CONST.autoCompltHintSelectedClass:
							tStyles = input_autoComplt_list.styles.autoCompltHintSelected;
							adjStyleAttrs = _CONST.adjStyleAttrs.autoCompltHintSelected;
						break;
					}

					if (styles instanceof Object && tStyles && adjStyleAttrs) {
						
						for (var i = 0; i < adjStyleAttrs.length; i++) {
							
							if (typeof styles[adjStyleAttrs[i]] == "string" || typeof styles[adjStyleAttrs[i]] == "number") { // A simple type checking
								if (!newStyles) {
									newStyles = {};
								}
								newStyles[adjStyleAttrs[i]] = tStyles[adjStyleAttrs[i]] = styles[adjStyleAttrs[i]];
							}
							
						}						
					
					}
					
					return newStyles;
				}
				
				input.autoComplt.close = function () {
					input_autoComplt_currentTarget = ""; // Closing means no need for autocomplete hint so no autocomplete target either
					input_autoComplt_list.close();
				}
				
				input.autoComplt.enable = function () {
					input_autoComplt_enabled = true;
				}
				
				input.autoComplt.disable = function () {
					this.close();
					input_autoComplt_enabled = false;
				}
				
				input.autoComplt.destroy = function () {
					_rmEvent(input, "blur", input_autoComplt_blurEvtHandle);
					_rmEvent(input, "keyup", input_autoComplt_keyEvtHandle);
					_rmEvent(input, "keydown", input_autoComplt_keyEvtHandle);
					this.close();
					delete input.autoComplt;
				}
				
				_addEvt(input, "blur", input_autoComplt_blurEvtHandle);
				_addEvt(input, "keyup", input_autoComplt_keyEvtHandle);
				_addEvt(input, "keydown", input_autoComplt_keyEvtHandle);
				
				if (params instanceof Object) {
					input.autoComplt.config(params);
					input.autoComplt.setHintsFetcher(params.hintsFetcher);
				}
				
				return input;
			}
			return null;
		}
		
	};

	return publicProps;
}());
