function sample() {

    var s = new Sidebar();
    s.name =            "David Forsythe";
    s.occupation =      "Former Computer Programmer";
    s.status = [
        {level: "crit", text: "You have some nasty wounds and scratches,", icon: "fa-plus"},
        {level: "high", text: "your heart is pounding,", icon: "fa-heart"},
        {level: "med",  text: "your ears are ringing,", icon: "fa-frown-o"},
        {level: "low",  text: "and damn, you could really use a shower.", icon: "fa-frown-o"}
    ];
    s.equipment = {
        "Body":         "FreeBSD T-shirt",
        "Legs":         "Unintentionally Ripped Jeans",
        "Feet":         "Snowboard Boots",
        "Head":         "Motorcycle Helmet",
        "Arms":         "-",
        "Neck":         "-",
        "Waist":        "-",
        "Shoulders":    "-",
        "L. Finger":    "-",
        "R. Finger":    "-"
    }
    s.hands = {
        "L. Hand": {
            name:       'GPS Device'
        },
        "R. Hand": {
            name:       'Heckler & Koch MP5',
            amount:     17,
            capacity:   30
        }
    }
    s.pack = {
        name:           "Alice Pack",
        amount:         20,
        capacity:       50
    }
    s.inventory = [
        {type: "money", icon: "fa-bitcoin", name: "Wallet", description: "17 bitcoins"},
        {type: "medicine", icon: "fa-medkit", name: "Small Medkit", description: "+25HP"},
        {type: "medicine", icon: "fa-medkit", name: "Large Medkit", description: "+100HP"},
        {type: "food", icon: "fa-cutlery", name: "Pickled Egg", description: "+10HP"},
        {type: "food", icon: "fa-cutlery", name: "Rotten Apple", description: "+1HP"},
        {type: "food", icon: "fa-cutlery", name: "Can of Beans", description: "+20HP"},
        {type: "book", icon: "fa-book", name: "\"Power Moves\"", description: "dforsyth's autobiography"},
        // {type: "drink", icon: "fa-beer", name: "2 Empty Beer Steins"},
        // {type: "potion", icon: "fa-flask", name: "Cloudy Potion"},
        // {type: "potion", icon: "fa-flask", name: "Glowing Potion"},
        // {type: "weapon", icon: "fa-magic", name: "Feather Duster"},
        // {type: "weapon", icon: "fa-magic", name: "Winchester Rifle"},
        // {type: "weapon", icon: "fa-magic", name: "Crowbar"},
        // {type: "weapon", icon: "fa-gavel", name: "Warhammer"},
        // {type: "weapon", icon: "fa-shield", name: "Hylian Shield"},
        // {type: "key", icon: "fa-key", name: "Dusty Key"},
        // {type: "key", icon: "fa-key", name: "Orange Key"},
    ]

    s.render();

    var d1 = new Description("You are at the intersection of <b>First</b> Avenue and <b>Sussex</b> Drive.");
    d1.text = "You feel hemmed in by the lonely skyscrapers surrounding you. <b>Sussex</b> drive \
        heads north from here and <b>First</b> avenue continues to the east and west. The \
        <b>door</b> to the building on the south side of the street looks ajar. \
        <span class=\"info\">You smell smoke.</span>";

    var d2 = new Description("You are in the lobby of a downtown skyscraper.");
    d2.text = "Your heart is pounding, and your ears are ringing. A door opens to First Avenue to \
    the north. There are rooms to the west and east. \
    <span class=\"info\">You hear zombies outside!</span>";

    var c1 = new Command('east',        'You head east along First Avenue.');
    var c2 = new Command('look',        'You look at your surroundings.');
    var c3 = new Command('fire',        'You point your MP5 at the disgusting zombies to the north.');
    var c4 = new Command('get mag',     'You quickly snatch up the 9mm magazine and slam in into your MP5! \
        <span class="sound-2x">&mdash;CLUNK&mdash;  &nbsp;&nbsp;&nbsp;  CHHK-CHHK!</span>');
    var c5 = new Command('run',         'You run towards the only safe direction, the door to your south.');
    var c6 = new Command('close door',  'You slam the door shut, and engage the deadbolt. \
        <span class="sound-2x">SLAM!</span>');

    var ol1 = new List("object");
    ol1.items.push({icon: "fa-male",         text: "<b>mjard</b> is here, just southeast of you"});
    ol1.items.push({icon: "fa-briefcase",    text: "A <b>9mm magazine</b> lays on the ground."});
    ol1.items.push({icon: "fa-users",        text: "a pair of <b>zombies</b> approach from <b>Sussex</b>!"});
    ol1.items.push({icon: "fa-users",        text: "a group of four <b>zombies</b> approach from <b>First</b> to the east!"});
    ol1.items.push({icon: "fa-users",        text: "a lone <b>zombie</b> approaches from <b>First</b> to the west!"});

    var ol2 = new List("object");
    ol2.items.push({icon: "fa-male",         text: "<b>mjard</b> is here, just southwest of you"});
    ol2.items.push({icon: "fa-building-o",   text: "An aluminum door opens to the street outside, where you can see zombies approaching!"});

    var al1 = new List("action");
    al1.items.push({icon: "fa-bolt",         text: "mjard scrambles through the <b>door</b> to the south."});
    al1.items.push({icon: "fa-bolt",         text: "Zombies approach from the north, east and west! They are only 9 meters away!"});

    var al2 = new List("action");
    al2.items.push({icon: "fa-bolt",         text: "Zombies approach from the north, east and west! They are only 5 meters away!"});

    var il1 = new List("info");
    il1.items.push({icon: "fa-eye",         text: "You spot a <b>9mm magazine</b> laying on the ground nearby!"});

    var cl1 = new List("conversation");
    cl1.items.push({icon: "fa-quote-left",         text: "<b>mjard says</b> \"holy fuck.\""});
    cl1.items.push({icon: "fa-quote-right",         text: "<b>You say</b> \"wheres your gun?\""});
    cl1.items.push({icon: "fa-quote-left",         text: "<b>mjard says</b> \"umm...\""});

    var combat1 = new Combat(text="You unleash a hail of automatic gunfire! \
        <span class=\"sound\">RAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT!</span> \
        Both zombies take hits! One of them was shot cleanly between the eyes! It crumples to the \
        ground gurgling and convulsing. The other is hit in the torso. It is stunned for a moment, \
        but continues to shamble towards you! You have 13 bullets remaining in your MP5.");

    var combat2 = new Combat(text="You unleash a hail of automatic gunfire towards the zombie to the north! \
        <span class=\"sound\">RAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT!</span> \
        <span class=\"sound-3x\">&mdash;CLICK&mdash;</span> \
        The zombie is cut to ribbons by your accurate firing! It's remaining body parts spill \
        across the street. Your MP5 is now empty!");

    var combat3 = new Combat(text="You point your MP5 at the grotesque zombies to the east. You \
        unleash a hail of automatic gunfire! \
        <span class=\"sound\">RAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT-TAT!</span> \
        Three of the zombies take hits in the torso and arms. They are stunned for a moment, but \
        continue to shamble towards you! You have 17 bullets remaining in your MP5.");

    var w = new Window("trading");
    w.text = "Mjard asks to take your <b><i class=\"fa fa-magic\"></i> Heckler &amp; Koch MP5</b> in \
        exchange for <b><i class=\"fa fa-cutlery\"></i> 2 Cans of Beans</b>. Lorem ipsum dolor sit \
        amet, consectetur adipisicing elit. Repellat, eius, dolorum dignissimos officia mollitia \
        quidem exercitationem praesentium veritatis ad fuga optio sapiente molestiae debitis maxime \
        hic nisi iusto quam esse."

    d1.render();
    c1.render();
    d1.render();
    ol1.render();
    al1.render();
    c2.render();
    d1.render();
    ol1.items.splice(0, 1);
    ol1.render();
    c3.render();
    combat1.render();
    // al1.items.splice(0, 1);
    al2.render();
    combat2.render();
    il1.render();
    c4.render();
    combat3.render();
    c5.render();
    d2.render();
    ol2.render();
    c6.render();
    cl1.render();
    w.render();
}
