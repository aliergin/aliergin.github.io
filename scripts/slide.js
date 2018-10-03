// -----------------------------------------------
//   --->   Ultimate Javascript Slideshow   <---
//   --->   Author: Znupi                   <---
//   --->   Contact: znupi69@gmail.com      <---
// -----------------------------------------------
imgs1 = [[ "images/mae1.png", "images/mae3.png", "images/mae5.png", "images/mae7.png", "images/mae9.png", "images/mae11.png" ]];
var ss1 = new SlideShow(imgs1, 'slide1DIV', 5, 30, 0.05);

imgs2 = [[ "images/mae2.png", "images/mae4.png", "images/mae6.png", "images/mae8.png", "images/mae10.png", "images/mae12.png" ]];
var ss2 = new SlideShow(imgs2, 'slide2DIV', 5, 30, 0.05);

//>>>>>>>>Parameters explanation>>>>>>>>
//
//1. The first parameter is a multidimensional array,
//   each child-array being an 'image set'. The slideshow
//   will start with the first set. Note: if you only want
//   one image set, you will still have to declare a
//   multi-dimensional array, like [ [ 'image1.gif', 'image2.gif'] ].
//2. The second argument is the div's id in which you must have an
//   image. Example markup:
//   <div id="slideDIV"><img src="" alt="Slideshow"></div>
//   In this case, your second argument will be 'slideDIV'. Also, you
//   will need some CSS to it, so here's the minimum CSS to use:
//   div#slideDIV {
//			background: url('load.gif') 50% 50% no-repeat #000; /* for the loading image */
//			width: 320px; /* same as images */
//			height: 240px; /* same as images */
//			line-height: 0; /* fix IE space below image */
//		}
//		div#slideDIV img {
//			opacity: 0; /* So it doesn't show while loading */
//			filter: alpha(opacity=0); /* the same, for IE */
//		}
//3. The third argument is the pause between two images. Literally the time
//   from when an image stops fading in, to when it starts fading out. (seconds)
//4. The fourth argument is the delay between two frames. The lower value this has,
//   the faster the fading between images is. (miliseconds)
//5. The last argument is the 'step'. The amount of opacity that changes between
//   two frames, basically the higher value, the faster but the rougher the animation.
//   This has to be between 0 and 1. If set to 1, there will be no animation at all.
//(*) I recommend you use 2, 20-50, 0.05 as the last three arguments.
//
//<<<<<<<<Parameters explanation<<<<<<<<
//
//>>>>>>>>Changing the image set>>>>>>>>
//
//To change the 'image set', you have to just call a simple function. For example,
//if you defined your slideshow like "var mySlideShow = new SlideShow(imgs, 'somediv', 2, 20, 0.05),
//you will have to call "mySlideShow.chgImgSet(1)" to change to the second image set.
//Example HTML: <a href="javascript:void(0)" onclick="mySlideShow.chgImgSet(1)">View the second set of images</a>
//
//<<<<<<<<Changing the image set<<<<<<<<

function SlideShow(aImg, sID, iPause, iDelay, iStep) {
	var imgs = aImg;
	var preLoadObjs = Array();
	var loadedImgs = 0;
	var totalImgs= 0;
	var pause = iPause;
	var delay = iDelay;
	var step = iStep;
	var curIndex = 0;
	var curImgSet = 0;
	var curOpc = 1;
	var curDir = 0;
	var tOut = null;
	var sID = sID;
	var oDIV = null;
	var oIMG = null;
	var i;
	this.init = function() {
		oDIV = document.getElementById(sID);
		oIMG = oDIV.getElementsByTagName("img")[0];
		for (i=0; i < imgs.length; i++) totalImgs += imgs[i].length;
		for (i=0; i < imgs.length; i++) {
			for (j=0; j < imgs[i].length; j++) {
				preLoadObjs[preLoadObjs.length] = new Image();
				preLoadObjs[preLoadObjs.length-1].src = imgs[i][j];
				if (!window.opera) { 
                                   preLoadObjs[preLoadObjs.length-1].onload = countLoadedImgs;
                                   countLoadedImgs();
                                }
				if (i == imgs.length-1 && j == imgs[i].length-1 && window.opera) {
					start();
				}
			}
		}
	}
	var countLoadedImgs = function() {
		loadedImgs++;
		if (loadedImgs == totalImgs) start();
	}
	var start = function() {
		oIMG.src = imgs[curImgSet][0];
                //if (oIMG.style.MozOpacity) oIMG.style.MozOpacity = 1;
                oIMG.style.opacity = "1";
		if (window.ActiveXObject) oIMG.style.filter = "alpha (opacity=100)";
		curOpc = 1;
		oDIV.style.backgroundImage = "url('" + imgs[curImgSet][1] + "')";
		curIndex++;
                if (sID == "slide2DIV")	tOut = setTimeout(doSlide, (pause+2)*1000);
                else 			tOut = setTimeout(doSlide, pause*1000);
	}
	var doSlide = function() {
		if (!curDir) {
			curOpc-=step;
                        //if (oIMG.style.MozOpacity) oIMG.style.MozOpacity = curOpc;
                        oIMG.style.opacity = curOpc;
			if (window.ActiveXObject) oIMG.style.filter = "alpha (opacity=" + (curOpc*100) + ")";
			if (curOpc > 0) tOut = setTimeout(doSlide, delay);
			else {
				changeImgs();
				curDir = 1;
				tOut = setTimeout(doSlide, pause*1000);
			}
		}
		else {
			curOpc+=step;
                        //if (oIMG.style.MozOpacity) oIMG.style.MozOpacity = curOpc;
                        oIMG.style.opacity = curOpc;
			if (window.ActiveXObject) oIMG.style.filter = "alpha (opacity=" + (curOpc*100) + ")";
			if (curOpc < 1) tOut = setTimeout(doSlide, delay);
			else {
				changeImgs();
				curDir = 0;
				tOut = setTimeout(doSlide, pause*1000);
			}
		}
	}
	var changeImgs = function() {
		if (curIndex < imgs[curImgSet].length-1) curIndex++;
		else curIndex = 0;
		if (!curDir) {
			oIMG.src = imgs[curImgSet][curIndex];
			curOpc = 0;
                        //if (oIMG.style.MozOpacity) oIMG.style.MozOpacity = 0;
                        oIMG.style.opacity = "0";
		}
		else oDIV.style.backgroundImage = "url('" + imgs[curImgSet][curIndex] + "')";
	}
	this.chgImgSet = function(newImgSet) {
		if (newImgSet != curImgSet) {
			clearTimeout(tOut);
			curImgSet = newImgSet;
			curIndex = 0;
			start();
		}
	}
}
