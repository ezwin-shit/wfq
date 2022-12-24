import random,string, base64
# API Starter
from waitress import serve
# Flask Shit
import requests
from flask import Flask, request, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify, make_response
# Faker Shit
from faker import Faker
from faker.providers import internet


# create a Flask app
app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3600000 per day", "6000 per hour"],
    storage_uri="memory://",
)

@app.route('/', methods=['GET'])
@limiter.limit("10000000 per year")
def api():
    
    return{
        'fakecc': '/fakecc',
        'color' : '/color',
        'useragent' : '/useragent',
        'fakeperson': '/fakeperson',
        'randemail' : '/randemail',
        'randip': '/randip',
        'randaddy': '/randaddy',
        'randpass': '/randpass'
    }


@app.route('/meme', methods=['GET'])
@limiter.limit("1000 per minute")
def meme():
    r = requests.get('https://www.reddit.com/r/memes/new.json?sort=hot')
    res = r.json()
    return {
        'Url': res['data']['children'][random.randint(0, 25)]['data']['url']
    }


@app.route('/fakecc', methods=['GET'])
@limiter.limit("1000 per minute")
def fakecc():
    fake = Faker()
    
    expiremonth = random.randint(1,12)  
    expireyear = random.randint(23,30)
    
    if expiremonth < 10:
        jizz = f"0{expiremonth}/{expireyear}"
    else:
        jizz = f"{expiremonth}/{expireyear}"

    
    return {
        'Provider': fake.credit_card_provider(),
        'Numbers': fake.credit_card_number(),
        'Expire': jizz,
        'Security': fake.credit_card_security_code()
    }

@app.route('/color', methods=['GET'])
@limiter.limit("1000 per minute")
def color():
    fake = Faker()
    
    return {
        'colorname': fake.color_name(),
        'color': fake.color(),
        'hex': fake.hex_color(),
        'safehex': fake.safe_hex_color(),
        'rgb': fake.rgb_color(),
        'rgbcss': fake.rgb_css_color(),
        'hsv': fake.color(color_format='hsv'),
        'hsl': fake.color(color_format='hsl'),
    }

@app.route('/useragent', methods=['GET'])
@limiter.limit("1000 per minute")
def useragent():
    fake = Faker()
    
    return{
        'useragent': fake.user_agent(),
        'chrome': fake.chrome(),
        'firefox': fake.firefox(),
        'opera': fake.opera(),
        'safari': fake.safari(),
        'internetexplorer': fake.internet_explorer(),
        'ios': fake.ios_platform_token(),
        'linux': fake.linux_platform_token(),
    }

@app.route('/name', methods=['GET'])
@limiter.limit("1000 per minute")
def name():
    fake = Faker()
    
    return{
        'male':{
            'malefirst': fake.first_name_male(),
            'malelast': fake.last_name_male()
        },
        'female':{
            'femalefirst': fake.first_name_female(),
            'femalelast': fake.last_name_female()
        }
    }

@app.route('/discordidlookup', methods=['POST'])
@limiter.limit("1000 per minute")
def discordidlookup():
    
    user_id = request.args.get('id')
    token = "MTAyMTQ4MDA5MzIxNTg4MzI4NA.G4e4c3.pgOultM_-EpPb4PyCUQ45oWYEaFopzuaFRoGH8"

    r = requests.get("https://canary.discord.com/api/v9/users/" + user_id, headers={"Authorization": token})

    avatar = 'https://cdn.discordapp.com/avatars/' + user_id + "/"
    if avatar == "null":
        avatar = "doesnt have one"
    elif avatar !="null":
        avatar = 'https://cdn.discordapp.com/avatars/' + user_id + "/" + r.json()["avatar"] + ".png"

    if r.status_code == 200:
        return {
            'username': r.json()['username'],
            'discriminator': '#' +r.json()['discriminator'],
            'userid': r.json()['id'],
            'fullusername': r.json()['username'] + "#" + r.json()['discriminator'],
            'avatar': avatar,
            'Flags': str(r.json()['public_flags'])
        }
    else:
        return {
            'ERROR': 'ERROR!!'
        }

@app.route('/fakeperson', methods=['GET'])
@limiter.limit("1000 per minute")
def fakeperson():
    fake = Faker()
    expiremonth = random.randint(1,12)  
    expireyear = random.randint(23,30)
    
    if expiremonth < 10:
        jizz = f"0{expiremonth}/{expireyear}"
    else:
        jizz = f"{expiremonth}/{expireyear}"
    fake = Faker('en_US')

    gbfake = Faker('en_GB')
    addresuk = gbfake.address()
    addresreplaceduk = addresuk.replace('\n', ' ')

    usfake = Faker('en_US')
    addresus = usfake.address()
    addresreplacedus = addresus.replace('\n', ' ')


    return {
        'person': {
            'firstname': fake.first_name(),
            'lastname': fake.last_name(),
            'us_address': addresreplacedus,
            'uk_address': addresreplaceduk,
            'city': fake.city(),
            'phone': fake.phone_number(),
            'dateofbirth': fake.date_of_birth(),
        },
        'job':{
            'company': fake.company(),
            'job': fake.job()
        },
        'cc': {
            'Provider': fake.credit_card_provider(),
            'Numbers': fake.credit_card_number(),
            'Expire': jizz,
            'Security': fake.credit_card_security_code(),
        }
    }



@app.route('/randemail', methods=['GET'])
@limiter.limit("1000 per minute")
def randemail():
    fake = Faker()
    return{
        'email': fake.free_email()
    }
    
@app.route("/getmyip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route('/randip', methods=['GET'])
@limiter.limit("1000 per minute")
def randip():
    fake = Faker()
    fake.add_provider(internet)

    
    return {
        'ip': fake.ipv4_private()
    }
   
@app.route('/yomama', methods=['GET'])
@limiter.limit("1000 per minute")
def yomama():
 
    yomamaso = ["Yo momma so fat were in her right now","Yo momma so fat people jog around her for exercise","Yo momma so fat she went to the movies and sat next to everyone","Yo momma so fat she has been declared a natural habitat for Condors","Yo mamma so fat you haveta roll over twice to get off her...","Yo momma so fat she was floating in the ocean and spain claimed her for then new world","Yo momma so fat she lay on the beach and people run around yelling Free Willy","Yo momma so fat when you get on top of her your ears pop!","Yo momma so fat when she has sex, she has to give directions!","Yo momma so fat she goes to a resturant, looks at the menu and says \"okay!\"","Yo momma so fat when she wears a yellow raincoat, people said \"Taxi!\"","Yo momma so fat she had to go to Sea World to get baptized","Yo momma so fat she got to iron her pants on the driveway","Yo momma so fat she put on her lipstick with a paint-roller","Yo momma so fat she got to pull down her pants to get into her pockets","Yo momma so fat when she tripped over on 4th Ave, she landed on 12th","Yo momma so fat when she bungee jumps, she brings down the bridge too","Yo momma so fat the highway patrol made her wear \"Caution! Wide Turn\"","Yo momma so fat when she sits around the house, she SITS AROUND THE HOUSE!","Yo momma so fat when she steps on a scale, it read \"one at a time, please\"","Yo momma so fat when she sits on my face I can't hear the stereo.","Yo momma so fat she fell in love and broke it.","Yo momma so fat when she gets on the scale it says to be continued.","Yo momma so fat when she gets on the scale it says we don't do livestock.","Yo momma so fat whenever she goes to the beach the tide comes in!","Yo momma so fat when she plays hopscotch, she goes New York, L.A.,  Chicago...","Yo momma so fat she's got Amtrak written on her leg.","Yo momma so fat even Bill Gates couldn't pay for her liposuction!","Yo momma so fat her legs is like spoiled milk - white & chunky!","Yo momma so fat you have to roll her ass in flour and look for the wet spot to fuck her!","Yo momma so fat I had to take a train and two buses just to get on the bitches good side!","Yo momma so fat she wakes up in sections!","Yo momma so fat when she goes to an amusement park, people try to ride HER!","Yo momma so fat she sat on a quarter and a booger shot out of george washington's nose.","Yo momma so fat she was mistaken for God's bowling ball!","Yo momma so fat she rolled over 4 quarters and it made a dollar!","Yo momma so fat when she lies on the beach no one else gets sun!","Yo momma so fat when she bunje jumps she goes straight to hell!","Yo momma so fat when she jumps up in the air she gets stuck!!!","Yo momma so fat she's got more Chins than a Hong Kong phone book!","Yo momma so fat that her senior pictures had to be arial views!","Yo momma so fat she's on both sides of the family!","Yo momma so fat everytime she walks in high heels, she strikes oil!","Yo momma so fat she fell and made the Grand Canyon!","Yo momma so fat she sat on the beach and Greenpeace threw her in!","Yo momma so fat the animals at the zoo feed her.","Yo momma so fat she was baptized at Marine World.","Yo momma so fat she's on both sides of the family!","Yo momma so fat when she dances at a concert the whole band skips.","Yo momma so fat the Aids quilt wouldn't cover her","Yo momma so fat she stands in two time zones.","Yo momma so fat I tried to drive around her and I ran out of gas.","Yo momma so fat she left the house in high heels and when she came back she had on flip flops.","Yo momma so fat shes on both sides of the family.","Yo momma so fat it takes her two trips to haul ass","Yo momma so fat you have to grease the door frame and hold a twinkie on the other side just to get her through","Yo momma so fat when the bitch goes to an all you can eat buffet, they have to install speed bumps.","Yo momma so fat that she cant tie her own shoes.","Yo momma so fat sets off car alarms when she runs.","Yo momma so fat she cant reach her back pocket.","Yo momma so fat when she wears one of those X jackets, helicopters try to land on her back!","Yo momma so fat her college graduation picture was an airial.","Yo momma so fat she broke her leg, and gravy poured out!","Yo momma so fat when she rides in a hot air balloon, it looks like she's wearin tights!","Yo momma so fat she got hit by a parked car! ","Yo momma so fat they have to grease the bath tub to get her out!","Yo momma so fat she has a run in her blue-jeans!","Yo momma so fat when she gets on the scale it says to be continued.","Yo momma so fat when she wears a yellow raincoat people say \"Taxi!\"","Yo momma so fat she got to iron her pants on the driveway!","Yo momma so fat she put on her lipstick with a paint-roller!","Yo momma so fat when she tripped over on 4th Ave she landed on 12th","Yo momma so fat when she bungee jumps she pulls down the bridge too","Yo momma so fat she steps on a scale & it goes one at a time please","Yo momma so fat she fell in love and broke it!","Yo momma so fat she jumped up in the air and got stuck!","Yo momma so fat she fell in love and broke it.","Yo momma so fat when she sits on my face I can't hear the stereo.","Yo momma so fat she eats Wheat Thicks.","Yo momma so fat her neck looks like a pair of hot dogs!","Yo momma so fat she's got her own area code!","Yo momma so fat she looks like she's smuggling a Volkswagon!","Yo momma so fat God couldn't light Earth till she moved!","Yo momma so fat NASA has to orbit a satellite around her!","Yo momma so fat that when she hauls ass, she has to make two trips!","Yo momma so fat even her clothes have stretch marks!","Yo momma so fat she has a wooden leg with a kickstand!","Yo momma so fat she has to use a VCR as a beeper!","Yo momma so fat they use the elastic in her underwear for bungee jumping","Yo momma so fat when they used her underwear elastic for bungee jumping, they hit the ground.","Yo momma so fat when she back up she beep.","Yo momma so fat she jumped up in the air and got stuck.","Yo momma so fat she has to buy two airline tickets.","Yo momma so fat when she fell over she rocked herself asleep trying to get up again.","Yo momma so fat she influences the tides.","Yo momma so fat that when I tried to drive around her I ran out of gas.","Yo momma so fat she broke her leg and gravy fell out.","Yo momma so fat she lays on the beach and greenpeace tried to push her back in the water","Yo momma so fat she broke her leg and gravy poured out","Yo momma so fat she uses redwoods to pick her teeth","Yo momma so fat the only pictures you have of her are satellite pictures","Yo momma so fat she jumped in the air and got stuck.","Yo momma so fat she put on some BVD's and by the time they reached her waist they spelled out boulevard.","Yo momma so fat she sat on a dollar and squeezed a booger out George Washington's nose.","Yo momma so fat she stepped on a rainbow and made Skittles.","Yo momma so fat she uses a mattress for a tampon.","Yo momma so fat that when she sits on the beach, Greenpeace shows up and tries to tow her back into the ocean.....","Yo momma so fat that she would have been in E.T., but when she rode the  bike across the moon, the bitch caused an eclipse.","Yo momma so fat she hoola-hooped the super bowl.","Yo momma so stupid that she puts lipstick on her head just to make-up her mind","Yo momma so stupid she hears it's chilly outside so she gets a bowl","Yo momma so stupid you have to dig for her IQ!","Yo momma so stupid she got locked in a grocery store and starved!","Yo momma so stupid it took her 2 hours to watch 60 Minutes!","Yo momma so stupid that she tried to put M&M's in alphabetical order!","Yo momma so supid she could trip over a cordless phone!","Yo momma so stupid she sold her car for gasoline money!","Yo momma so stupid she bought a solar-powered flashlight!","Yo momma so stupid she thinks a quarterbacks a refund!","Yo momma so stupid she took a cup to see Juice.","Yo momma so stupid that she sold the car for gas money.","Yo momma so stupid she asked you \"What is the number for 911\"?","Yo momma so stupid she took a ruler to bed to see how long she slept.","Yo momma so stupid when she read on her job application to not write below the dotted line she put \"O.K.\"","Yo momma so stupid she got stabbed in a shoot out.","Yo momma so stupid she stole free bread.","Yo momma so stupid she took a spoon to the superbowl.","Yo momma so stupid she called Dan Quayle for a spell check.","Yo momma so stupid she stepped on a crack and broke her own back.","Yo momma so stupid she makes Beavis and Butt-Head look like Nobel Prize winners.","Yo momma so stupid she thought she needed a token to get on Soul Train.","Yo momma so stupid when asked on an application, \"Sex?\", she marked, \"M, F and sometimes Wednesday too.\"","Yo momma so stupid she took the Pepsi challenge and chose Jif.","Yo momma so stupid when you stand next to her you hear the ocean!","Yo momma so stupid she hears it's chilly outside so she gets a bowl","Yo momma so stupid she got locked in a grocery store and starved!","Yo momma so stupid she thinks Fleetwood Mac is a new hamburger at McDonalds!","Yo momma so fat when her beeper goes off, people thought she was backing up","Yo momma so fat her nickname is \"DAMN\"","Yo momma so fat she was baptised in the ocean.","Yo momma so fat she has to iron her clothes in the driveway.","Yo momma so fat they tie a rope around her shoulders and drag her through a tunnel when they want to clean it.","Yo momma so fat when she got hit by a bus, she said, \"Who threw that rock?\"","Yo momma so fat when she stands in a left-turn lane it gives her the green arrow!","Yo momma so fat that when whe was born, she gave the hospital stretch marks.","Yo momma so fat the National Weather Agency has to assign names to her farts!!!","Yo momma so fat we went to the drive-in and didn't have to pay because we dressed her as a Chevrolet.","Yo momma so stupid it took her 2 hours to watch 60 minutes","Yo momma so stupid when she saw the NC-17 (under 17 not admitted) sign, she went home and got 16 friends","Yo momma so stupid when your dad said it was chilly outside, she ran outside with a spoon","Yo momma so stupid she told everyone that she was \"illegitiment\" because she couldn't read","Yo momma so stupid she sits on the TV, and watches the couch!","Yo momma so stupid that she thought Boyz II Men was a day care center.","Yo momma so stupid she bought a videocamera to record cable tv shows at home.","Yo momma so stupid when she went to take the 44 bus, she took the 22 twice instead.","Yo momma so stupid she jumped out the window and went up.","Yo momma so stupid she thought a quarterback was an income tax refund.","Yo momma so stupid she took a umbrella to see Purple Rain.","Yo momma so stupid that under \"Education\" on her job apllication, she put \"Hooked on Phonics.\"","Yo momma so stupid she put out the cigarette butt that was heating your house.","Yo momma so stupid she put lipstick on her forehead, talking about she was trying to makeup her mind.","Yo momma so stupid she watches \"The Three Stooges\" and takes notes.","Yo momma so ugly when she joined an ugly contest, they said \"Sorry, no professionals.\"","Yo momma so ugly she looks out the window and got arrested for mooning.","Yo momma so ugly just after she was born, her mother said \"What a treasure!\" and her father said \"Yes, let's go bury it.\"","Yo momma so ugly they push her face into dough to make gorilla cookies.","Yo momma so ugly they filmed \"Gorillas in the Mist\" in her shower","Yo momma so ugly they didn't give her a costume when she tried out for Star Wars.","Yo momma so ugly instead of putting the bungee cord around her ankle, they put it around her neck","Yo momma so ugly she gets 364 extra days to dress up for Halloween.","Yo momma so ugly when she walks into a bank, they turn off the surveillence cameras","Yo momma so ugly her mom had to be drunk to breast feed her","Yo momma so ugly her mom had to tie a steak around her neck to get the dogs to play with her.","Yo momma so ugly when she walks down the street in September, people say \"Damn, is it Halloween already?\"","Yo momma so ugly the government moved Halloween to her birthday.","Yo momma so ugly that if ugly were bricks she'd have her own projects.","Yo momma so ugly they pay her to put her clothes on in strip joints.","Yo momma so ugly she made an onion cry.","Yo momma so ugly they filmed \"Gorillas in the Mist\" in her shower!","Yo momma so ugly when they took her to the beautician it took 12 hours. . .for a quote!","Yo momma so ugly they put her in dough and made monster cookies!","Yo momma so ugly she tried to take a bath the water jumped out!","Yo momma so ugly she looks out the window and gets arrested!","Yo momma so ugly even Rice Krispies won't talk to her!","Yo momma so ugly Ted Dansen wouldn't date her!","Yo momma so ugly for Halloween she trick or treats on the phone!","Yo momma so ugly she had to get her baby drunk to breastfeed it!","Yo momma so ugly she turned Medusa to stone!","Yo momma so ugly The NHL banned her for life","Yo momma so ugly she gets 364 extra days to dress up for Halloween!","Yo momma so ugly the government moved Halloween to her birthday!","Yo momma so ugly if ugly were bricks she'd have her own projects!","Yo momma so ugly they pay her to put her clothes on in strip joints","Yo momma so ugly she made an onion cry!","Yo momma so ugly people go as her for Halloween.","Yo momma so ugly that when she sits in the sand on the beach, cats try to bury her.","Yo momma so ugly she scares the roaches away.","Yo momma so ugly we have to tie a steak around your neck so the dog will play with her!","Yo momma so ugly I heard that your dad first met her at the pound.","Yo momma so ugly that if ugly were bricks she'd have her own projects.","Yo momma so ugly that your father takes her to work with him so that he doesn't have to kiss her goodbye.","Yo momma so old I told her to act her own age, and the bitch died.","Yo momma so old she has Jesus' beeper number!","Yo momma so old her social security number is 1!","Yo momma so old that when God said let the be light, she hit the switch'","Yo momma so old that when she was in school there was no history class.","Yo momma so old she owes Jesus 3 bucks!","Yo momma so old she's in Jesus's yearbook!","Yo momma so old she has a picture of Moses in her yearbook.","Yo momma so old her birth certificate says expired on it.","Yo momma so old she knew Burger King while he was still a prince.","Yo momma so old she owes Jesus a nickel.","Yo momma so old when God said \"Let their be light\", she flipped the switch.","Yo momma so old she was a waitress at the Last Supper.","Yo momma so old she ran track with dinosaurs.","Yo momma so old her birth certificate is in Roman numerals.","Yo momma so old she has a picture of Moses in her yearbook.","Yo momma so old she sat behind Jesus in the third grade.","Yo momma so old and stupid she knew the Virgin Mary when she was 10 and said, \"Li'l Mary will never amount to anything\".","Yo momma so poor when I saw her kicking a can down the street, I asked her what she was doing, she said \"Moving.\"","Yo momma so poor she can't afford to pay attention!","Yo momma so poor when I ring the doorbell I hear the toilet flush!","Yo momma so poor when she goes to KFC, she has to lick other people's fingers!!!","Yo momma so poor when I ring the doorbell she says,\"DING!\"","Yo momma so poor she went to McDonald's and put a milkshake on layaway.","Yo momma so poor she went to McDonald's and put a milkshake on layaway.","Yo momma so poor your family ate cereal with a fork to save milk.","Yo momma so poor she goes to Kentucky Fried Chicken to lick other people's fingers.","Yo momma so poor her face is on the front of a foodstamp.","Yo momma so poor she was in K-Mart with a box of Hefty bags.  I said, \"What ya doin'?\" She said, \"Buying luggage.\"","Yo momma so poor she drives a peanut.","Yo momma so poor she waves around a popsicle stick and calls it air conditioning.","Yo momma so dark she went to night school and was marked absent!","Yo momma so dark she spits chocolate milk!","Yo momma so dark she went to night school and was marked absent.","Yo momma so dark that she can leave fingerprints on charcoal.","Yo momma so dark she has to wear white gloves when she eats Tootsie Rolls to keep from eating her fingers.","Yo momma so dirty she has to creep up on bathwater.","Yo momma so short she poses for trophies!","Yo momma so short you can see her feet on her drivers lisence!","Yo momma so short she has to use a ladder to pick up a dime.","Yo momma so short she can play handball on the curb.","Yo momma so short she does backflips under the bed.","Yo momma so short she models for trophys.","Yo momma so nasty when she goes to a hair salon, she told the stylist to cut her hair and she opened up her shirt","Yo momma so nasty She gotta put ice down her drawers to keep the crabs fresh!","Yo momma so nasty she made speed stick slow down.","Yo momma so nasty she brings crabs to the beach","Yo momma so nasty she made right guard turn left.","Yo momma so nasty the fishery be paying her to leave","Yo momma so nasty she has to creep up on bathwater.","Yo momma so nasty that her shit is glad to escape.","Yo momma so nasty Ozzie Ozbourne refused to bite her head off","Yo momma so nasty that pours salt water down her pants to keep her crabs fresh.","Yo momma so nasty I called her for phone sex and she gave me an ear infection.","Yo momma like potato chips-- Fri-to Lay","Yo momma like a screen door, after a couple bangs she tends to loosen up! ","Yo momma like the pillbury doughboy - everyone gets a poke!","Yo momma like a doorknob - everyone gets a turn!","Yo momma like a T.V. set, even a three year old can turn her on!","Yo momma like a doorknob, everyone gets a turn!","Yo momma like a bus, fifty cents and she's ready to ride!","Yo momma like a golf course, everyone GETS a hole in one!","Yo momma like the railway system, she gets laid all over the country!","Yo momma like a tomato source bottle, everyone gets a squeeze out of her!","Yo momma like a shotgun: one cock and she blows!","Yo momma like a hardware store: 4 cents a screw!","Yo momma like Domino's pizza-- Something for nothing","Yo momma like a refridgerator: everyone likes to put their meat in her!","Yo momma like cake mix, 15 servings per package!","Yo momma like a rifle... four cocks and she's loaded.","Yo momma like a bowling ball.  She's picked up, fingered, and then thrown in the gutter.","Yo momma like a bus:  Guys climb on and off her all day long.","Yo momma like a Toyota: \"Oh what a feelin'!\"","Yo momma like Orange Crush: \"Good Vibrations!\"","Yo momma like a bubble-gum machine... five cents a blow.","Yo momma like chinese food:  sweet, sour and cheap!","Yo momma like a vaccuum cleaner.....a real good suck.","Yo momma so hairy you almost died of rugburn at birth!","Yo momma so hairy she's got afros on her nipples!","Yo momma so hairy she look like she got Buchwheat in a headlock.","Yo momma so hairy Bigfoot is taking her picture!","Yo momma so hairy she wears a Nike tag on her weave so now everybody calls her Hair Jordan.","Yo momma so slutty she could suck-start a Harley!","Yo momma so slutty she could suck the chrome off a trailer hitch ball!","Yo momma so slutty when she got a new mini skirt, everyone commented on her nice belt!","Yo momma so slutty she was on the cover of wheaties, with her legs open, and it said \"breakfast of the champs\" ","Yo momma so slutty that I could've been your daddy, but the guy in line behind me had the correct change.","Yo momma so slutty she had her own \"Hands across her ass\" charity drive","Yo momma so slutty that when she heard Santa Claus say HO HO HO she thought she was getting it three times.","Yo momma so slutty I fucked her and I's a chick!","Yo momma so slutty she blind and seeing another man.","Yo momma nose so big you can go bowling with her boogers!","Yo momma nose so big she makes Pinochio look like a cat!","Yo momma so greasy she used bacon as a band-aid!","Yo momma so greasy she sweats Crisco!","Yo momma so greasy Texaco buys Oil from her","Yo momma teeth are so yellow traffic slows down when she smiles!","Yo momma teeth are so yellow she spits butter!","Yo momma so lazy she thinks a two-income family is where yo daddy has two jobs.","Yo momma so skinny she hula hoops with a cheerio","Yo momma so skinny she has to wear a belt with spandex.","Yo momma so skinny she turned sideways and dissapeared.","Yo momma so bald even a wig wouldn't help!","Yo momma so bald you can see whats on her mind","Yo momma so bald that she took a shower and got brain-washed.","Yo momma so tall she tripped over a rock and hit her head on the moon.","Yo momma so tall she did a back-flip and kicked Jesus in the mouth.","Yo momma so tall she tripped in Michigan and hit her head in Florida.","Yo momma so flat she's jealous of the wall!","Yo momma's glasses are so thick that when she looks on a map she can see people waving.","Yo momma's glasses are so thick she can see into the future.","Yo momma has an afro with a chin strap.","Yo momma has one leg and a bicycle.","Yo momma has 4 eyes and 2 pair of sunglasses.","Yo momma has so much hair on her upper lip, she braids it.","Yo momma has one hand and a Clapper.","Yo momma has a wooden afro with an \"X\" carved in the back.","Yo momma has green hair and thinks she's a tree.","Yo momma has one ear and has to take off her hat to hear what you're saying.","Yo momma has a 'fro with warning lights.","Yo momma has 10 fingers--all on the same hand.","Yo momma has a glass eye with a fish in it.","Yo momma has a short leg and walks in circles.","Yo momma has a short arm and can't applaude.","Yo momma got so many freckles she looks like a hamburger!","Yo momma got two wooden legs and one is one backward.","Yo momma got three fingers and a banjo.","Yo momma got a wooden leg with a kickstand on it.","Yo momma got a bald head with a part and sideburns.","Yo momma got a' afro, wit' a chin strap!!!!","Yo momma got a wooden leg with branches.","Yo momma house so small you have to go outside to change your mind.","Yo momma house so dirty roaches ride around on dune buggies!","Yo momma house so dirty she has to wipe her feet before she goes outside.","Yo momma hair so short when she braided it they looked like stiches.","Yo momma hair so short she curls it with rice.","Yo momma head so big she has to step into her shirts.","Yo momma head so big it shows up on radar.","Yo momma head so small she use a tea-bag as a pillow.","Yo momma head so small that she got her ear pierced and died.","Yo momma wears knee-pads and yells \"Curb Service!\"","Yo momma feet are so big her shoes have to have license plates!","Yo momma aint so bad...she would give you the hair off of her back!","Yo momma lips so big, Chap Stick had to invent a spray.","It took yo momma 10 tries to get her drivers license, she couldnt get used to the front seat!","Yo momma hips are so big, people set their drinks on them.","Yo momma hair so nappy she has to take Tylenol just to comb it.","Yo momma so clumsy she got tangled up in a cordless phone.","Yo momma so wrinkled, she has to screw her hat on.","Yo momma twice the man you are.","Yo momma cross-eyed and watches TV in stereo.","Yo momma is missing a finger and can't count past 9.","Yo momma arms are so short, she has to tilt her head to scratch her ear.","Yo momma middle name is Rambo.","Yo momma in a wheelchair and says, \"You ain't gonna puch me 'round no more.\"","Yo momma rouchy, the McDonalds she works in doesn't even serve Happy Meals.","Yo momma so stupid was born on Independence Day and can't remember her birthday.","Yo momma mouth so big, she speaks in surround sound.","Yo momma gums are so black she spits Yoo-hoo.","Yo momma breath smell so bad when she yawns her teeth duck.","Yo momma teeth are so rotten, when she smiles they look like dice.","Yo mamma so fat, she wore a X t-shirt, and a helicopter landed on her","Yo mamma so skinny, she hang glides with a Dorito","Yo mamma so stupid, she thinks hamburger helper comes with another person","Yo mamma so stupid, she thinks menopause is a button"]
 
    return {
        'yomamaso': random.choice(yomamaso)
    }
 
@app.route('/insult', methods=['GET'])
@limiter.limit("1000 per minute")
def insult():
    
    insults = ["I'll  hit you so hard by the time you come down, you'll need a passport and a plane ticket back!","I'll hit you so hard you 'll have to take off your shoes to shit!","I'll hit you so hard you'll have to unzip your pants to say hi!","I'll hit you so hard your kids will be born dizzy!","I'll hit you so hard your wife will fall!","You're so dumb you think socialism means partying!","You're so dumb you think manual labor is a Mexican!","You're so dumb you think Johnny Cash is a pay toilet!","You're so dumb it takes you an hour and a half to watch \"60 Minutes\"!","You  so stupid you probably think Taco Bell is where you pay your telephone bill.","You so dumb you got blonde roots in your eyeballs.","Your so stupid, that you got fired from the M & M factory for throwing away all the W's.","Your so stupid, that you went to a Clippers game to get a hair cut.","Your so stupid, that you went to a Whalers game to see Shamu.","Your so stupid, it takes you an hour to cook minute rice.","She  was  so ugly...  they used to push her face into dough to make gorilla biscuits","You're so ugly you'd make a train take a dirt road!","You're so ugly when you walk into a bank, they turn the cameras off!","You're  so  ugly,  if you stuck your head out the window, they'd arrest you for mooning!","You're  so  ugly  if  you  joined  an  ugly  contest, they'd say \"Sorry, no professionals!\"","You're so ugly your face is closed on weekends!","You're so ugly you could be the poster child for abortion/birth control!","You're so ugly if my dog looked like you, I'd shave its ass and teach it to walk backwards!","You're so ugly when you were born the doctor slapped your mother!","You're  so ugly when you were born, your mother saw the afterbirth and said \"Twins!\"","You're so ugly they know what time you were born, because your face stopped the clock!","She's so ugly she could scare the moss off a rock!","She's so ugly she could scare the chrome off a bumper!","Your face so so ugly when you cry the tears run up your face.","Your so ugly, your mother had to feed you with a sling shot.","Your  so  ugly,  your mother had to tie a steak around your neck to get the dog to play with you.","You're so fat when you sit around the house, you sit AROUND the HOUSE","You're so fat a picture of you would fall off the wall!","You're  so  fat  if  you  weighed  five  more  pounds,  you could get group insurance!","You're  so  fat  you  get  clothes in three sizes:  extra large, jumbo, and oh-my-god-it's-coming-towards-us!","You're so fat if you got your shoes shined, you'd have to take his word for it!","Your  so  fat,  that you have to strap a beeper on your belt to warn people you are backing up.","Your so fat, that you have to use a mattress as a maxi-pad.","Your wife said she liked seafood.  So I gave her crabs.","Are those your tits, or did Laurel and Hardy leave you their heads?","Is that an accent, or is your mouth just full of sperm?","If I had change for a buck, I could have been your dad!","You're so skinny, that you use a bandaid as a maxi-pad.","You're like a light switch, even a little kid can turn you on.","I'm  looking forward to the pleasure of your company since I haven't had it yet.","When you pass away and people ask me what the cause of your death was, I'll say your stupidity.","Well I'll see you in my dreams - if I eat too much.","I've  had  many  cases  of love that were just infatuation, but this hate I feel for you is the real thing.","You're the best at all you do - and all you do is make people hate you.","Don't you realize that there are enough people to hate in the world already without your working so hard to give us another?","The  thing that terrifies me the most is that someone might hate me as much as I loathe you.","When you get run over by a car it shouldn't be listed under accidents.","All of your ancestors must number in the millions; its hard to believe that many people are to blame for producing you.","Ever since I saw you in your family tree I've wanted to cut it down.","I  hear  that  when  you were a child your mother wanted to hire someone to take care of you but the Mafia wanted too much.","I  hear that when your mother first saw you she decided to leave you on the front steps of a police station while she turned herself in.","You  were  born  because  your  mother  didn't believe in abortion; now she believes in infanticide.","No  one should be punished for accident of birth but you look too much like a wreck not to be.","Yours was an unnatural birth; you came from a human being.","You  were the answer to a prayer.  Your parents prayed that the world would be made to suffer and here you came along.","You're a habit I'd like to kick; with both feet.","I hear the only place you're ever invited is outside.","I would like the pleasure of your company but it only gives me displeasure.","You've never been outspoken; no one has ever been able to.","At  your speed you'd better not stop your mouth too fast or your teeth will fly through your cranium.","If you ever tax your brain, don't charge more than a penny.","Don't you have a terribly empty feeling ---- in your skull?","You  have  nothing  to fear from my baser instincts; its my finer ones that tell me to kill you.","It's your life --- but I wish you'd let us have it.","I  don't  consider you a vulture.  I consider you something a vulture would eat.","I  think you should live for the moment.  But after that I doubt I'll think so.","Man you're alive!  But I wish you weren't.","I  believe in respect for the dead; in fact I could only respect you if you WERE dead.","I  admire  your because I've never had the courage it takes to be a liar, a thief and a cheat.","You're acquitting yourself in such a way that no jury ever would.","You have a face only a mother could love - and she hates it!","You never strike out blindly; you fail in the light.","Roses are red, violets are blue, i have 5 fingers and the middle one is for You.","Yo mommas so dumb she stopped at a stop sign and waited for it to say go!","Yo mama so dumb she stared at da orange juice bottle cause it said concentrate","Your momma is so fat that when she stepped on the scale it said one at a time please.","Yo mammas so fat you could slap her legs and ride the waves","Yo mama so dumb she sold her car for gas money","Yo Mama's so fat, she got baptized at Sea World.","You're mom's so stupid, she got locked up in a super market and starved","Yo Momma is so fat she walked out in high heels and came back in flip flops.","Yo' Momma's So Fat When her beeper goes off, people think she's backing up.","Yo mama's so fat when she ordered a water bed they layed a blanket on the Pacific Ocean","Yo mamma's like a shotgun, one cock and she blows.","Yo mama so dumb that when I said \"christmas is just around the corner\" she went looking for it!","Yo Mamma's so fat it takes two busses and a train to get on her good side.","Your mom is so stupid, I said it's chilly outside, your mom ran outside wit a bowl and a spoon and asked where??","Yo Momma so fat she stepped on da scale and and it said to be continued...","Yo Mama's so poor, when I was asking why she was banging on the dumpster she said, \"My kids locked me out.\"","Yo Momma so dumb when she saw a bus with white people in it she said, \"Go catch that twinky.\"","Yo mommas so fat, she has to use a matress for a tampon.","Yo mamma's so stupid, she jumped off a boat and missed the water.","Yo mama's so fat, when she stepped on the dog's tail we had to change his name to Beaver.","Yo momma's so fat that when she goes outside in her yellow jacket people say \"Look it's the magic school bus!!!\"","Yo Mamma so fat that when the school bus drives by she yells STOP THAT TWINKIE!","Yo Mama so fat she went into a zoo and a zookeeper said, \"Oh boy...another elephant got out!\"","Yo mamma so stupid, it took her two hours to watch 60 minutes","Yo mamma is like a brick, flat on both sides and gets laid by mexicans!","Yo mama's so fat that when she went to wal-mart she tripped over k-mart and hit target!!!!:-D","Yo momma is so fat, she stepped on a dollar and made change.","Yo mama's so poor when I saw her kickin' a can down the street, I asked her what was she doing and she said she was movin'","Your mammas so stupid she got locked in mattress store and slept on the floor.","Yo mama so fat she sat on a rainbow and skittles came out....","Your mama is so fat she jumped in to the ocean and the whales stated to sing we are family.","Yo mama's so fat she has her own zipcode","Yo Momma is like a doornob, everyone gets a turn.","Yo mamma's so fat she fell in love and broke it","Yo Mama's so fat, when she stepped onto the scale it said \"to infinity and beyond!\"","Yo Momma so fat, when she went to swim in the ocean she said \"Oops I'm in the kiddy pool!\"","I thought you were ugly ... and then I met your mama","Yo Mamma is like a hockey playa, she doesnt changer her pads for 3 periods!","Yo Momma's so ugly on Halloween, people go as her.","Yo momma's so fat that when she jumped for joy she got stuck!","Yo Momma is so fat that her cereal bowl comes with a lifeguard.","Yo' mama so fat, she has to make a long distance call to talk to herself!","Yo Momma so fat her tanning bed was Mexico!","Your momma is so retarded she got stabbed in a shootout.","Yo momma's so fat, she walked in front of the t.v and I missed a whole series of friends!","Yo momma is so fat, she's taller sideways.","Yo Mamma so stupid that she went to Dr. Dre for liposuction.","Yo Momma so dumb, she sat on the TV to watch the couch","Yo momma's so fat, she uses the pacific ocean to take a bath.","I'm not here... but yo mama is ;-)","Yo Momma's so horny, when she found out Winnie the Pooh had no pants, she a got a boner.","Yo momma so greasy they hired her at the cinima to put the butter on the popcorn!","Yo Momma so stupid her favorite color is clear.","Yo mamas so fat that at the circus she nicknamed the elephant pee wee.","Your momma's so fat that when she fell in the forest, the loggers said \"TIMBER\"!","Your momma is so fat that when she sweats she can be used as a steam roller.","Your momma's so fat she has to use the ocean as her toilet!","Hey!! they made a song about your weight 8675309","I called your boyfriend gay and he hit me with his purse!","Roses are red violets are blue, God made me pretty, what the hell happen to you?","Right now I'm sitting here looking at you trying to see things from your point of view but I can't get my head that far up my ass.","If you didn't have feet you wouldn't wear shoes.....then why do you wear a bra??!","mirrors don't talk but lucky for you %n they don't laugh","Poof be gone, your breath is too strong, I don't wanna be mean, but you need listerine, not a sip, not a swallow, but the whole friggin bottle","People like you are the reason I'm on medication.","Don't piss me off today, I'm running out of places to hide to bodies","I have always woundered why people bang their heads against brick walls..... then I met you. Don't bother leaving a message.","Don't let your mind wander. It's way to small to be outside by itself!","I had a nightmare. I dreamt I was you.","Hey, Remember that time I told you I thought you were cool? I LIED.","I need you...........I want you............To get out of my face. Damn not you again.......","Everyone is entitled to be stupid, but you abuse the privilege.","If I wanted to talk to you, I would have called you first.","I am not anti-social..I just don't like you","If you're gonna act like a dick you should wear a condom on your head so you can at least look like one !!!","Hmm...I dont know what your probelm is...but I'm going to bet it's really hard to pronounce...","There are some stupid people in this world. You just helped me realize it.","Until you called me I couldn't remember the last time I wanted somebody's fingers to break so badly.","If you ran 1,000,000 miles to see the boy/girl of your dreams, what would you say when you got there?","Wow, you looked a lot hotter from a distance!","Cancel my subscriptions ... I'm tired of your issues.","I may be fat,but you're ugly,and I can diet!!!","Earth is full. Go home.","If I could be one person for a day, it sure as hell wouldn't be you.","Hey, heres a hint. If i don't answer you the first 25 times, what makes you think the next 25 will work?","How do you keep an idiot in suspense? Leave a message and I'll get back to you...","Oh dear! Looks like you fell out of the ugly tree and hit every branch on the way down!","What's that ugly thing growing out of your neck... Oh... It's your head...","I'm sorry, Talking to you seems as appealing as playing leapfrog with unicorns.","Oh I'm sorry, how many times did your parents drop you when you were a baby?","Don't hate me because I'm beautiful hate me because your boyfriend thinks so.","God made mountains, god made trees, god made you but we all make mistakes.","Remember JESUS loves you but everyone else thinks you're an idiot.","I'm not mean ... you're just a sissy.","Sorry I can't think of an insult stupid enough for you.","Why don't you go outside any play, hide and go f**k yourself","Beauty is skin deep, but ugly is to the bone","How about a little less questions and a little more shut the hell up? I'm away live with it.","FOR THE LAST TIME! Your mother left here at 9 this morning... Leave me alone!","Let's see, I've walked the dog, cleaned my room, gone shopping and gossiped with my friends...Nope, this list doesn't say that I'm required to talk to you.","When you were born you were so ugly that instead of slapping you, the doctor slapped your mom! leave a message","My Mom said never talk to strangers and well, since you're really strange.... I guess that means I can't talk to you!","Forget the ugly stick! you must have been born in the ugly forrest!","I really don't like you but if you really must leave a message, I'll be nice and at least pretend to care.","You know the drill! You leave a message....and I ignore it!","The Village just called. They said they were missing their town idiot, I couldn't really understand them, but I think they were saying the name was yours...","I'm not here right now so cry me a river, build yourself a bridge, and GET OVER IT!!!","Why are you bothering me? I have my away message on cause I don't want to listen to you and your stupid nonsense.","You dont know me, you just wish you did.","Hey- I am away from my computer but in the meantime, why don't you go play in traffic?!","You have your whole life to be a jerk....so why dont you take a day off so.. leave me a message for when I get back!!!!"]
    
    
    
    return {
        'insult': random.choice(insults)
    }
        

@app.route('/randaddy', methods=['GET'])
@limiter.limit("1000 per minute")
def randaddy():
    gbfake = Faker('en_GB')
    addresuk = gbfake.address()
    addresreplaceduk = addresuk.replace('\n', ' ')

    usfake = Faker('en_US')
    addresus = usfake.address()
    addresreplacedus = addresus.replace('\n', ' ')

    return {
        'name': gbfake.name(),
        'uk_address': addresreplaceduk,
        'us_address': addresreplacedus
    }   

@app.route('/randchoice', methods=['POST'])
@limiter.limit("1000 per minute")
def randchoice():
    choice1 = request.args.get('choice1')
    choice2 = request.args.get('choice2')

    randomchoice = random.choice([choice1, choice2])

    return{
        'choice': randomchoice
    }
    
@app.route('/randint', methods=['POST'])
@limiter.limit("1000 per minute")
def randint():
    fake = Faker()
    number = request.args.get('length')
    
    return{
        'number': fake.random_number(digits=int(number))
    }
    
@app.route('/randintrange', methods=['POST'])
@limiter.limit("1000 per minute")
def randintrange():
    number1 = request.args.get('min')
    number2 = request.args.get('max')
    if int(number1) > int(number2):
        return{
            'ERROR': 'number1 has to be smaller than number2'
        }
    else:
        randomnumber = random.randint(int(number1),int(number2))
        return {
            'number': randomnumber
        }

@app.route('/username', methods=['GET'])
def usernamename():
    invalidnamejson = {
        'Valid': 'False',
        'Error': 'Please Contact an Administrator if this is not correct'
    }
    validnamejson = {
        'Valid': True
    }
    name = request.args.get('name')
    message_bytes = name.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    encodedusername = base64_bytes.decode('ascii')
    if encodedusername in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/name.txt', 'r'):
        return make_response(jsonify(validnamejson), str(200))
    elif encodedusername not in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/name.txt', 'r'):
        return make_response(jsonify(invalidnamejson), str(404))
    
@app.route('/key',methods=['GET'])
def key():
    keyvalid = {
        'Valid': True   
    }
    keyinvalid = {
        'Valid': 'False',
        'Error': 'Please Contact an Administrator if this is not correct'
    }
    key = request.args.get('key')      
    message_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    encodedkey = base64_bytes.decode('ascii')
    if encodedkey in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/keys.txt', 'r'):
        return make_response(jsonify(keyvalid), str(200))
    elif encodedkey not in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/keys.txt', 'r'):
        return make_response(jsonify(keyinvalid), str(404))
                
@app.route('/hwid', methods=['GET'])
def hwid():
    hwid = request.args.get('hwid')
    message_bytes = hwid.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    encodedhwid = base64_bytes.decode('ascii')
    jizz = open("C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/blacklist.txt", "a")
    valid = {
        'Valid': True
    }
    invalid = {
        'Success': 'False',
        'HWID': 'Invalid HWID'
    }
    blacklistjson = {
        'Valid': 'False',
        'Error': 'You Are Hwid Blacklisted'
    }
    if encodedhwid in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/blacklist.txt', 'r'):
        return make_response(jsonify(blacklistjson), str(404))  
    elif encodedhwid in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/hwid.txt', 'r'):
        return make_response(jsonify(valid), str(200))
    elif encodedhwid not in open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/hwid.txt', 'r'):
        jizz.write(encodedhwid + '\n')
        return make_response(jsonify(invalid), str(404))
    
        """
        with open(r'C:/Users/sricc/OneDrive/Desktop/Discord Trolling Tools/api/hwid.txt', 'r') as fp:
            lines = fp.readlines()
            for hwidline in lines:
                if hwidline.find(encodedhwid) != -1:
                    return {
                            'Vaild': 'True',
                            'lineNumber': lines.index(hwidline),
                        }
                else:
                    return make_response(jsonify(invalid), str(404))
        """
    


@app.route('/passgen', methods=['POST'])
@limiter.limit("1000 per minute")
def randpass():
    
    specialcharacters = request.args.get('punctuation')
    amount = request.args.get('amount')
    
    
    trueorfalseerror= {
            'ERROR': 'Special Character Choice can only be True or False',
            'Note': 'The true or false can also be True or False with caps'
    }
    
    notlengthyenough = {
        'ERROR': 'Please put amount greater than 10 or equal to 10 for a secure password.'
    }
    
    
    if specialcharacters == "true" or specialcharacters == "True":
        random_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(int(amount)))
    elif specialcharacters == "false" or specialcharacters == "False":
        random_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(int(amount)))    
    else:
        return make_response(jsonify(trueorfalseerror), str(404))

    if int(amount) < 10:
        return make_response(jsonify(notlengthyenough), str(404))
    else:
        return {
            'password': random_password
        }
        

if __name__ == '__main__':
    print("Api is up and running - 127.0.0.1:5000")
    #app.run(ip="77.68.54.160",port=6969,debug=True) 
    serve(app, port=6969)
    