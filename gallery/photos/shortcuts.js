
// Some variables to autodetect browser type
var ns=(document.layers);
var ie=(document.all);
var w3=(document.getElementById && !ie);

var timeout=5000;
var help_isshow=0;
var fullscreen_mode=0;

// Return an object
function get_object(id)
{
 if(!ns && !ie && !w3) 
   return null;
 if (ie)
   e=eval("document.all." + id);
 else if (ns)
   e=eval('document.links[id]');
 else if (w3)
   e=eval('document.getElementById(id)');
 return e;
}

// Return the style of an object
function get_object_style(id)
{
  var style = null;
  if (ie)
    style=eval('document.all.'+id+'.style');
  else if (ns)
    style=eval('document.layers[id]');
  else if (w3)
    style=eval('document.getElementById(id).style');
  return style;
}


function add_arg_to_url(url, arg, value)
{
  if (url.indexOf('?')>0)
    url += '&' + arg + '=' + value;
  else
    url += '?' + arg + '=' + value;
  return url;
}

// Change the current page to the id found in the page
function jumpto(id)
{
  e = get_object(id);
  if ((e != null) && (e.href != null)) {
    var url = e.href;
    if (mytimeout)
      url = add_arg_to_url(url, 'slideshow', timeout);
    if (fullscreen_mode)  {
      url = add_arg_to_url(url, 'fullscreen', '1');
      url += '#image';
    } 
    location.href = url;
  }
}

// Change the current page
function next_page()
{
  jumpto('next_link');
}

function previous_page()
{
  jumpto('previous_link');
}


function show_navbar()
{
  navbar_style = get_object_style('navbar');
  if (ie || w3)
    navbar_style.visibility="visible";
  else if (ns)
    navbar_style.visibility="show";
}

function hide_navbar()
{
  navbar_style = get_object_style('navbar');
  if (ie || w3)
    navbar_style.visibility="collapse"; // don't work in konqueror
  else if (ns)
    navbar_style.visibility="hide";
}

function show_help_layer()
{
  help_layer_style = get_object_style('helpwindow');

  if (ie)
   {
     documentWidth=document.body.offsetWidth/2+document.body.scrollLeft-20;
     documentHeight=document.body.offsetHeight/2+document.body.scrollTop-20;
     help_layer_style.visibility="visible";
   }    
  else if (ns)
   {
     documentWidth=window.innerWidth/2+window.pageXOffset-20;
     documentHeight=window.innerHeight/2+window.pageYOffset-20;
     help_layer_style.visibility ="show";
   }
  else if (w3)
   {
     documentWidth=self.innerWidth/2+window.pageXOffset-20;
     documentHeight=self.innerHeight/2+window.pageYOffset-20;
     help_layer_style.visibility="visible";
   }
  help_layer_style.left=documentWidth-250;
  help_layer_style.top =documentHeight-125;
  help_isshow=1;
}

function hide_help_layer()
{
  help_layer_style = get_object_style('helpwindow');
  if (ie||w3)
    help_layer_style.visibility="hidden";
  else
    help_layer_style.visibility="hide";
  help_isshow=0;
  return false;
}

function toggle_help_layer()
{
  if (help_isshow)
   hide_help_layer();
  else
   show_help_layer();
  return false;
}

// Activate the fullscreen mode (works only in a new window)
function toggle_fullscreen()
{
  if (!fullscreen_mode)
   {
     var screen_width=screen.availWidth;
     var screen_height=screen.availHeight;
     var features='width='+screen_width;
     features += ',height='+screen_height;
     var url = add_arg_to_url(location.href, 'fullscreen', '1');
     url += '#image';
     window.open(url,'',features);
   }
  else
   {
     window.close();
   }
}


// Activate/Deactivate the slideshow
var mytimeout = 0;
function toggle_slideshow()
{
  if (!mytimeout)
   {
     mytimeout = setTimeout("next_page()",timeout);
     window.status='Slideshow set to ' + (timeout/1000) + ' seconds';
     e = get_object('slideicon');
     if ((e != null))
       e.src = "player_pause.png";
   }
  else
   {
     clearTimeout(mytimeout);
     mytimeout=0;
     window.status='Stopping Slideshow';
     e = get_object('slideicon');
     if ((e != null))
       e.src = "player_play.png";
   }
}

// Manage timeout for the slideshow
function modify_timeout(t)
{
  timeout+=t;
  if (timeout<1000)
    timeout=1000;
  if (mytimeout)
   { // If the counter is active, reactivate it !
    toggle_slideshow();
    toggle_slideshow();
   }
  else
   {
     window.status='Slideshow timeout set to ' + (timeout/1000) + ' seconds';
   }
}

// Event Handler that receive Key Event
function getkey(e)
{
  if (e == null)
   { // IE
     kcode = window.event.keyCode;
   } 
  else
   { // Mozilla
     kcode = e.which;
   }
  key = String.fromCharCode(kcode).toLowerCase();
  switch(key)
   {
     case "n":
     case " ":
       next_page();
       return false;
     case "p":
       previous_page();
       return false;
     case "s":
       toggle_slideshow();
       return false;
     case "+":
       modify_timeout(1000);
       return false;
     case "-":
       modify_timeout(-1000);
       return false;
     case "i":
       toggle_exif_window()
       return false;
     case "h":
     case "?":
       toggle_help_layer();
       return false;
   }
  switch(kcode)
   {
     case 8:
       previous_page();
       return false;
   }
  return true;
}

function common_init()
{
  if (typeof(exif_init) == "function")
    exif_init()
  // Get arguments parameters for this page
  var argstr = location.search.substring(1, location.search.length)
  var args = argstr.split('&');
  for (var i = 0; i < args.length; i++)
  {
    var arg = unescape(args[i]).split('=');
    if (arg[0] == "slideshow") 
     { // ... and set timeout according to the last value
       timeout=parseInt(arg[1]);
       toggle_slideshow();
     }
    else if (arg[0] == "fullscreen")
     {
       fullscreen_mode = 1;
       self.moveTo(0,0);
       self.resizeTo(screen.width,screen.height);
       //hide_navbar();
     }
  }
  // Some code for preloading the next image
  e = get_object('next_image');
  if ((e != null) && (e.href != null))
  {
    preload_image = new Image();
    preload_image.src = e.href;
  }
}

if(w3 || ie)
{
  document.onkeypress = getkey;
} 
else
{
  document.captureEvents(Event.KEYUP);
  document.onkeyup = getkey; 
  document.captureEvents(Event.KEYPRESS);
  document.onkeypress = getkey;
}

