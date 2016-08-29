
/*** CASPER ***/
var casper = require('casper').create({
    logLevel: "error",
    verbose: true,
    pageSettings: {
        loadImages: false,
        loadPlugins: false,
        userAgent: "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    },

    viewportSize: {width: 1024, height: 768},

    clientScripts: [
        'casper/includes/postings-concat.min.js',
    ],

});

casper.options.onResourceRequested = function(C, requestData, request) {
  if ((/https?:\/\/.+?\.css/gi).test(requestData['url']) || requestData['Content-Type'] == 'text/css') {
    //console.log('Skipping CSS file: ' + requestData['url']);
    request.abort();
  }
}

/*** ARGUMENTS ***/
require("utils");
var system = require('system');

var apiKey = system.env.CRAWLERA_APIKEY;

phantom.setProxy("proxy.crawlera.com", "8010", "manual", apiKey, "''");

var url = casper.cli.options['url'];

var pageObj = Object();

casper.start(url, function() {
    pageObj.httpStatus = this.status()['currentHTTPStatus'];
    pageObj.title = this.getTitle();
    pageObj.url = this.getCurrentUrl();
});



/*** TOOLS ***/
function replyButton(retry) {
        casper.waitForSelector("button.reply_button", function() {
            this.clickLabel("reply ");
            this.wait(2000, function() {
                pageObj.reply_options = this.evaluate(getReplyOptions);

                //this.echo("Checking reply options");
                if (pageObj.reply_options == null) {
                    //this.echo("NULL!!");
            
                    if (retry >= 3) {
                        pageObj.reply_options = "still error after 3 times"
                    } else {

                        this.reload(function(){
                            //this.echo("Reloaded....");
                            replyButton(retry+1);
                        });
                    }
                } else {
                    //this.echo("OK");
                }

            });
        }, function() { 
            pageObj.reply_options = "no reply options";
        });
};

function getBodyAttrs() {
    return document.querySelector("body").getAttribute("class");
}

function getReplyOptions() {
    buff = document.querySelector(".reply_options").innerText;
    buff = buff.replace(/(\r\n|\n|\r)/gm, ' ');
    return buff;
}

function getUserData() {
    buff = document.querySelector("#postingbody").innerText;
    buff = buff.replace(/(\r\n|\n|\r)/gm, ' ');
    return buff;
}

/*** FLOW ***/

/* Reply button. */
casper.then(function() {
    replyButton(1);
});


/* User data. */
casper.then(function() {
    this.waitForSelector(".showcontact", function() {
        pageObj.hidden_contact = true;
        this.clickLabel("show contact info");
    }, function() {
        pageObj.hidden_contact = false;
        //this.echo("No hidden contacts");
    });
    this.wait(5000, function() {
        pageObj.user_data = this.evaluate(getUserData);
    });
});

casper.run(function() {
    json_resp = JSON.stringify(pageObj);

    this.echo(json_resp);
    this.exit(0);
});
