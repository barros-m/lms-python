// Handles by client = STATIC
//loads and initialize the SDK of facebook
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; }
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

/*
    Things to do:

    -payment method
    -redirect user if connected to course page 
    -start developing the course page

*/
var person = { userID: "", name: "", accessToken: "", picture: "", email: ""};

function logIn() {
	window.location.href=("/login");
}

window.fbAsyncInit = function () {
    FB.init({
        appId: '1686727554790401',
        cookie: true,
        xfbml: true,
        version: 'v3.1'
    });

    FB.AppEvents.logPageView();

};


function register() {
    //window.location.href = ("http://facebook.com");// redirect top facebook page to make account
	window.location.href=("/register");

}

function request(){
    window.location.href=("/send_request"); 
}
