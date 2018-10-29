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
    FB.login(function (response) {
        if (response.status == "connected") {
            person.userID = response.authResponse.userID;
            person.accessToken = response.authResponse.accessToken;

            FB.api('/me?fields=id,name,email,picture.type(large)', function (userData) {
                person.name = userData.name;
                person.email = userData.email;
                person.picture = userData.picture.data.url;
                console.log(person.name, ": haha : ", person.email);
               
            });
            console.log("Redirecting...");
            window.location.href = ("/course.html");
        }
    }, {scope: 'public_profile, email'})
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


function makeAccount() {
    window.location.href = ("http://facebook.com");// redirect top facebook page to make account
}

function request(){
    console.log("No idea, how..."); 
}
