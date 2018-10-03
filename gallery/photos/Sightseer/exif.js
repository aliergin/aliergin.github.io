
var ns=(document.layers);
var ie=(document.all);
var w3=(document.getElementById && !ie);
var exif_layer;
var exif_isshow;

function exif_init()
{
   if(!ns && !ie && !w3) 
     return;
   if (ie)
     exif_layer=eval('document.all.exifwindow.style');
   else if (ns)
     exif_layer=eval('document.layers["exifwindow"]');
   else if (w3)
     exif_layer=eval('document.getElementById("exifwindow").style');
   
   exif_hide();
}

function exif_show()
{
  if (ie)
   {
     documentWidth  =document.body.offsetWidth/2+document.body.scrollLeft-20;
     documentHeight =document.body.offsetHeight/2+document.body.scrollTop-20;
     exif_layer.visibility="visible";
   }    
  else if (ns)
   {
     documentWidth=window.innerWidth/2+window.pageXOffset-20;
     documentHeight=window.innerHeight/2+window.pageYOffset-20;
     exif_layer.visibility ="show";
   }
  else if (w3)
   {
     documentWidth=self.innerWidth/2+window.pageXOffset-20;
     documentHeight=self.innerHeight/2+window.pageYOffset-20;
     exif_layer.visibility="visible";
   }
  exif_layer.left=documentWidth-150;
  exif_layer.top =documentHeight-125;
  exif_isshow=1;
  setTimeout("exif_hide()",10000);
}

function exif_hide()
{
  if (ie||w3)
    exif_layer.visibility="hidden";
  else
    exif_layer.visibility="hide";
  exif_isshow=0;
}

function toggle_exif_window()
{
  if (exif_isshow)
    exif_hide()
  else
    exif_show()
}
