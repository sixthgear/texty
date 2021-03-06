requirejs.config({
    appDir: ".",
    baseUrl: "static/js",
    paths: {
        'jquery': ['http://code.jquery.com/jquery-1.11.0.min', 'lib/jquery-1.11.0.min'],
        'bootstrap': ['http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min', 'lib/bootstrap.min'],
        'underscore': ['http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.6.0/underscore-min', 'lib/underscore-min'],
        'underscore-string': ['http://cdnjs.cloudflare.com/ajax/libs/underscore.string/2.3.3/underscore.string.min', 'lib/underscore.string.min'],
        'handlebars': ['http://cdnjs.cloudflare.com/ajax/libs/handlebars.js/1.3.0/handlebars', 'lib/handlebars'],
        'handlebars-truncate': ['lib/handlebars-truncate-helper'],
    },
    shim: {
        'handlebars-truncate' : ['handlebars'],
        'bootstrap' : ['jquery']
    }
});

require(['jquery', 'bootstrap', 'handlebars', 'handlebars-truncate'], function($) {
    init();
    return {};
});

function init() {

    var id = 0;
    var history = [];
    var forward = [];
    var host =  "ws://" + window.location.hostname + ":4000/websocket/" + id;

    // create global websocket
    websocket = new WebSocket(host);

    websocket.onopen = function(evt) {
        // console.log(evt)
    };

    websocket.onclose = function(evt) {
        // console.log(evt)
    };

    websocket.onmessage = function(evt) {

        var data = JSON.parse(evt.data);
        console.log(data);

        switch (data.type) {
            case "broadcast":
                var c = new Broadcast(data.text);
                c.render();
                break;
            case "command":
                var c = new Command(data.command, data.response);
                c.render();
                break;
            case "description":
                var c = new Description(data.intro, data.text);
                c.render();
                break;
            case "combat":
                var c = new Combat(data.text);
                c.render();
                break;
            case "character":
                for (d in data.character)
                    sidebar[d] = data.character[d];
                sidebar.render();
                break;
            default:
                var c = new List(data.type);
                c.items = data.items; // {text: data.text, icon: data.icon};
                for (item in c.items) {

                    if (!c.items[item].icon)
                        c.items[item].icon = 'icon';
                    else if (c.items[item].icon.indexOf('fa-')==0)
                        c.items[item].icon = 'fa '   + c.items[item].icon;
                    else if (c.items[item].icon.indexOf('icon-')==0)
                        c.items[item].icon = 'icon ' + c.items[item].icon;
                }
                c.render();
                break;
        }

        window.scrollTo(0,document.body.scrollHeight);
    };

    websocket.onerror = function(evt) {
        console.log(evt)
    };

    // set up handler to write to websocket when enter is pressed
    $(".command-input input").keydown(function(e){
        switch (e.which) {
            case 9:
                // console.log('tab')
                e.preventDefault();
                e.stopPropagation();
                // this.focus();
                break;
            case 13:
                var command = this.value.trim().substring(0,100);
                if (command) {
                    history = history.concat(forward);
                    forward = [];
                    history.push(command);
                    websocket.send(command);
                }
                this.value = "";
                break;
            case 38: // up
                e.preventDefault();
                e.stopPropagation();

                if (this.value && history.length)
                    forward.push(this.value);

                if (history.length)
                    $(this).val("").val(history.pop());


                break;
            case 40: // down
                e.preventDefault();
                e.stopPropagation();

                if (this.value)
                    history.push(this.value);

                if (forward.length)
                    $(this).val("").val(forward.pop());
                else
                    $(this).val("");

                break;
        }
    }).focus();

    // compile all templates
    templates = {
        "description":  Handlebars.compile($("#description-template").html()),
        "broadcast":    Handlebars.compile($("#broadcast-template").html()),
        "command":      Handlebars.compile($("#command-template").html()),
        "list":         Handlebars.compile($("#list-template").html()),
        "combat":       Handlebars.compile($("#combat-template").html()),
        "window":       Handlebars.compile($("#window-template").html()),
        "sidebar":      Handlebars.compile($("#sidebar-template").html())
    }

    sidebar = new Sidebar();
    sidebar.name = "...";
    sidebar.occupation = "...";
    sidebar.status = [
        {text: "You feel disconnected.", icon: "fa-frown-o"}
    ]
    sidebar.equipment = {};
    sidebar.pack = {'name': 'Nothing!', capacity: 0, amount: 0}
    sidebar.render();
}


// block class
var Block = function() {}
Block.prototype.render = function() {

    var output = $(".left-column");

    var element = $(this.template(this));
    // var str = element.html();
    // element.html('');

    // var i = 0;
    // var isTag;
    // var text;

    // (function type() {
    //     text = str.slice(0, ++i);
    //     if (text === str) return;
    //     element.html(text);
    //     var char = text.slice(-1);
    //     if( char === '<' ) isTag = true;
    //     if( char === '>' ) isTag = false;
    //     if (isTag) return type();
    //     setTimeout(type, 0.125);
    // }());

    output.append(element);

};

// sidebar class
var Sidebar = function() {
    this.template = templates.sidebar;
    // this.intro = intro;
    // this.text = text;
    return this;
}

Sidebar.prototype.render = function() {
    var output = $(".right-column");
    output.html(this.template(this));
};

// broadcast class
var Broadcast = function(text) {
    this.template = templates.broadcast;
    this.text = text;
    return this;
}
Broadcast.prototype = Block.prototype;

// description class
var Description = function(intro, text) {
    this.template = templates.description;
    this.intro = intro;
    this.text = text;
    return this;
}
Description.prototype = Block.prototype;

// command class
var Command = function(command, response) {
    this.template = templates.command;
    this.command = command;
    this.response = response;
    return this;
}
Command.prototype = Block.prototype;

// list class
var List = function(type) {
    this.template = templates.list;
    this.type = type;
    this.items = [];
    return this;
}
List.prototype = Block.prototype;

// combat class
var Combat = function(text) {
    this.template = templates.combat;
    this.text = text;
    return this;
}
Combat.prototype = Block.prototype;

// window class
var Window = function(type, title, text) {

    this.template = templates.window;
    this.type = type;
    this.title = title;
    this.text = text;
    this.buttons = [
        {label: 'Nope.',            type: 'danger',     icon: 'fa-times'},
        {label: 'Sure, Take it.',   type: 'success',    icon: 'fa-check'},
    ]
    return this;
}

Window.prototype = Block.prototype;

