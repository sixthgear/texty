requirejs.config({
    appDir: ".",
    baseUrl: "static/js",
    paths: {
        'jquery': ['http://code.jquery.com/jquery-1.11.0.min'],
        'bootstrap': ['http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min'],
        'underscore': ['http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.6.0/underscore-min'],
        'underscore-string': ['http://cdnjs.cloudflare.com/ajax/libs/underscore.string/2.3.3/underscore.string.min'],
        'handlebars': ['http://cdnjs.cloudflare.com/ajax/libs/handlebars.js/1.3.0/handlebars'],
        'handlebars-truncate': ['handlebars-truncate-helper']
    },
    shim: {
        'handlebars-truncate' : ['handlebars'],
        'bootstrap' : ['jquery']
    }
});

require(['jquery', 'bootstrap', 'handlebars', 'handlebars-truncate', 'sampledata'], function($) {
    init();
    return {};
});

function init() {

    // create global websocket
    var host = "ws://ironman.quitjobmakegames.com:4000/websocket";
    var host = "ws://texty.local:4000/websocket";
    websocket = new WebSocket(host);
    websocket.onopen = function(evt) {
        // this.send('look');
        console.log(evt)
    };
    websocket.onclose = function(evt) { console.log(evt) };

    websocket.onmessage = function(evt) {
        // console.log(evt.data);

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
                c.items = data.items;
                //({text: data.text, icon: data.icon});
                c.render();
                break;
        }

        window.scrollTo(0,document.body.scrollHeight);
    };

    websocket.onerror = function(evt) { console.log(evt) };

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
                if (command)
                    websocket.send(command);
                this.value = "";
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

    // load sample data
    // sample();
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
    output.append(this.template(this));
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

